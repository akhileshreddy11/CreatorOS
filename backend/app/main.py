from __future__ import annotations

import os
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.database import Approval, ErrorEvent, SessionLocal, init_db
from app.routers.ai import router as ai_router
from app.routers.operations import router as operations_router
from app.services.job_manager import JobManager
from app.services.validation.opportunity_safety_gate import OpportunitySafetyGate

init_db()

app = FastAPI(
    title="CreatorOS API",
    version="2.1.0",
    description="Approval-gated AI operating system for local-business lead generation.",
)

frontend_origins = [
    origin.strip()
    for origin in os.getenv(
        "CREATOROS_FRONTEND_ORIGINS",
        "http://localhost:3000,http://127.0.0.1:3000",
    ).split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=frontend_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ai_router)
app.include_router(operations_router)

jobs = JobManager()


class MissionApproval(BaseModel):
    approved: bool
    opportunity: dict | None = None


def _default_opportunity() -> dict:
    return {
        "topic": "Hyderabad gym trial-class enquiry campaign",
        "problem": "Local gym prospects need a clear reason to enquire and an easy next step.",
        "audience": ["Hyderabad gym owners", "beginners looking for a nearby class"],
        "strategy": "Create useful local-language short videos and route every CTA through an owner-approved follow-up.",
        "recommended_content": [
            "What to expect in your first gym trial class",
            "Three questions to ask before joining a Hyderabad gym",
            "A transparent introductory offer with a trial enquiry CTA",
        ],
        "product_idea": "",
    }


def _run_brief(job_id: str):
    from app.agents.business_partner import BusinessPartner

    jobs.update(job_id, stage="Initializing COO", progress=5)
    result = BusinessPartner().morning_brief()
    jobs.update(job_id, stage="Preparing CEO review", progress=95)
    return result


def _run_mission(job_id: str, opportunity: dict):
    from app.agents.mission_planner import MissionPlanner
    from app.services.mission_executor import MissionExecutor

    jobs.update(job_id, stage="Safety review", progress=10)
    safety_review = OpportunitySafetyGate().inspect(opportunity)
    if safety_review.get("status") != "SAFE":
        raise ValueError("Opportunity did not pass the safety gate and cannot be executed.")

    jobs.update(job_id, stage="Planning mission", progress=25)
    planner = MissionPlanner()
    mission = planner.create_mission(opportunity)

    jobs.update(job_id, stage="Executing approved tasks", progress=40)
    results = MissionExecutor().execute_mission(planner.task_manager.tasks)
    statuses = {result["task_id"]: result["status"] for result in results}
    for task in mission["tasks"]:
        task["status"] = statuses.get(task["id"], task["status"])

    mission["execution_status"] = (
        "COMPLETED"
        if results and all(result["status"] == "Completed" for result in results)
        else "FAILED"
    )
    jobs.update(job_id, stage="Recording approval", progress=90)
    return {
        "status": "APPROVED",
        "message": "Mission executed. Generated artifacts remain approval-gated and require owner review.",
        "mission": mission,
        "execution_results": results,
        "safety_review": safety_review,
    }


def _record_approval(status: str, reason: str) -> None:
    db = SessionLocal()
    try:
        db.add(
            Approval(
                resource_type="mission_opportunity",
                resource_id=0,
                status=status,
                action_class="approval_required",
                reason=reason,
                reviewed_by="owner",
                reviewed_at=datetime.now(timezone.utc),
            )
        )
        db.commit()
    finally:
        db.close()


@app.get("/")
def root():
    return {
        "message": "CreatorOS API is running.",
        "status": "success",
        "product": "Approval-gated local-business lead generation",
    }


@app.get("/health")
def health():
    try:
        db = SessionLocal()
        db.execute(__import__("sqlalchemy").text("SELECT 1"))
        db.close()
        return {"status": "healthy", "database": "ready"}
    except Exception:
        raise HTTPException(status_code=503, detail="CreatorOS database is unavailable.")


@app.get("/morning-brief")
def get_morning_brief():
    job = jobs.latest("morning_brief")
    if not job:
        return {"status": "NOT_STARTED", "message": "No morning brief has been generated yet."}
    response = {
        "status": {
            "PENDING": "STARTED",
            "RUNNING": "RUNNING",
            "COMPLETED": "READY",
            "FAILED": "FAILED",
        }.get(job["status"], job["status"]),
        "message": job["stage"],
        "job_id": job["job_id"],
        "progress": job["progress"],
        "stage": job["stage"],
        "started_at": job["started_at"],
        "completed_at": job["completed_at"],
    }
    if job["status"] == "COMPLETED":
        response["brief"] = job["result"]
    if job["status"] == "FAILED":
        response["error"] = job["error"]
    return response


@app.get("/morning-brief/{job_id}")
def get_morning_brief_job(job_id: str):
    job = jobs.get(job_id)
    if not job or job["type"] != "morning_brief":
        raise HTTPException(status_code=404, detail="Morning brief job not found.")
    return job


@app.post("/morning-brief/refresh")
def refresh_morning_brief():
    job = jobs.create("morning_brief", _run_brief)
    if job["status"] in {"PENDING", "RUNNING"}:
        return {
            "status": "STARTED" if job["status"] == "PENDING" else "RUNNING",
            "message": "CreatorOS COO is preparing the morning brief.",
            "job_id": job["job_id"],
            "progress": job["progress"],
            "stage": job["stage"],
        }
    return job


@app.post("/morning-brief")
def start_morning_brief():
    return refresh_morning_brief()


@app.post("/approve-mission")
def approve_mission(request: MissionApproval):
    opportunity = request.opportunity or _default_opportunity()

    if not request.approved:
        try:
            _record_approval("rejected", "CEO rejected opportunity.")
        except Exception as error:
            db = SessionLocal()
            try:
                db.add(ErrorEvent(severity="warning", component="mission_approval", message="Could not persist mission rejection."))
                db.commit()
            finally:
                db.close()
        return {"status": "REJECTED", "message": "Mission rejected by owner.", "next_step": "Review another opportunity."}

    safety_review = OpportunitySafetyGate().inspect(opportunity)
    if safety_review.get("status") != "SAFE":
        raise HTTPException(
            status_code=409,
            detail="Mission blocked by the opportunity safety gate; review the opportunity before approval.",
        )

    try:
        _record_approval("approved", f"CEO approved opportunity: {opportunity.get('topic', 'Opportunity')}")
    except Exception as error:
        raise HTTPException(status_code=503, detail="Mission approval could not be persisted safely.") from error

    job = jobs.create("mission", lambda job_id: _run_mission(job_id, opportunity))
    return {
        "status": "APPROVED",
        "message": "Mission approval recorded. Execution has started in the background; artifacts remain approval-gated.",
        "job_id": job["job_id"],
        "execution_status": job["status"],
        "safety_review": safety_review,
    }


@app.get("/missions/latest")
def get_latest_mission_job():
    job = jobs.latest("mission")
    if not job:
        raise HTTPException(status_code=404, detail="No mission has been started yet.")
    return job


@app.get("/missions/{job_id}")
def get_mission_job(job_id: str):
    job = jobs.get(job_id)
    if not job or job["type"] != "mission":
        raise HTTPException(status_code=404, detail="Mission job not found.")
    return job
