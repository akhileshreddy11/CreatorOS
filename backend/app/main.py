import os
import threading
import time
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.database import init_db
from app.routers.ai import router as ai_router
from app.routers.operations import router as operations_router


# ============================================================
# DATABASE
# ============================================================

init_db()


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="CreatorOS API",
    version="2.0.0",
    description=(
        "Approval-gated AI operating system "
        "for local-business lead generation."
    ),
)


# ============================================================
# CORS
# ============================================================

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


# ============================================================
# ROUTERS
# ============================================================

app.include_router(ai_router)
app.include_router(operations_router)


# ============================================================
# REQUEST MODELS
# ============================================================

class MissionApproval(BaseModel):
    approved: bool
    opportunity: dict | None = None


# ============================================================
# MORNING BRIEF STATE
# ============================================================

morning_brief_state = {
    "status": "NOT_STARTED",
    "result": None,
    "error": None,
    "started_at": None,
    "completed_at": None,
}

morning_brief_lock = threading.Lock()


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():
    return {
        "message": "CreatorOS API is running.",
        "status": "success",
        "product": "Approval-gated local-business lead generation",
    }


# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "database": "ready",
    }


# ============================================================
# BACKGROUND MORNING BRIEF WORKER
# ============================================================

def run_morning_brief():
    """
    Runs the expensive CreatorOS COO pipeline in a background
    thread so the HTTP request does not remain open while
    multiple Gemini requests are executing.
    """

    try:
        from app.agents.business_partner import BusinessPartner

        print()
        print("=" * 70)
        print("[COO] MORNING BRIEF STARTED")
        print("=" * 70)

        started = time.perf_counter()

        with morning_brief_lock:
            morning_brief_state["status"] = "RUNNING"
            morning_brief_state["result"] = None
            morning_brief_state["error"] = None
            morning_brief_state["started_at"] = (
                datetime.now(timezone.utc).isoformat()
            )

        # ----------------------------------------------------
        # RUN COMPLETE COO PIPELINE
        # ----------------------------------------------------

        result = BusinessPartner().morning_brief()

        elapsed = time.perf_counter() - started

        # ----------------------------------------------------
        # STORE RESULT
        # ----------------------------------------------------

        with morning_brief_lock:
            morning_brief_state["status"] = "READY"
            morning_brief_state["result"] = result
            morning_brief_state["completed_at"] = (
                datetime.now(timezone.utc).isoformat()
            )

        print(
            f"[COO] MORNING BRIEF COMPLETED "
            f"in {elapsed:.2f}s"
        )

        print("=" * 70)
        print("[COO] RESULT READY FOR OWNER REVIEW")
        print("=" * 70)
        print()

    except Exception as error:

        error_message = str(error)

        print()
        print("=" * 70)
        print("[COO] MORNING BRIEF FAILED")
        print(f"[COO] {error_message}")
        print("=" * 70)
        print()

        with morning_brief_lock:
            morning_brief_state["status"] = "FAILED"
            morning_brief_state["error"] = error_message
            morning_brief_state["completed_at"] = (
                datetime.now(timezone.utc).isoformat()
            )


# ============================================================
# MORNING BRIEF
# ============================================================

@app.get("/morning-brief")
def morning_brief():

    with morning_brief_lock:

        status = morning_brief_state["status"]

        # ----------------------------------------------------
        # ALREADY READY
        # ----------------------------------------------------

        if status == "READY":

            return {
                "status": "READY",
                "message": "Morning brief ready.",
                "brief": morning_brief_state["result"],
                "started_at": morning_brief_state["started_at"],
                "completed_at": morning_brief_state["completed_at"],
            }

        # ----------------------------------------------------
        # CURRENTLY RUNNING
        # ----------------------------------------------------

        if status == "RUNNING":

            return {
                "status": "RUNNING",
                "message": (
                    "CreatorOS COO is currently preparing "
                    "the morning brief."
                ),
                "started_at": morning_brief_state["started_at"],
            }

        # ----------------------------------------------------
        # PREVIOUSLY FAILED
        # ----------------------------------------------------

        if status == "FAILED":

            return {
                "status": "FAILED",
                "message": "Morning brief generation failed.",
                "error": morning_brief_state["error"],
            }

        # ----------------------------------------------------
        # FIRST EXECUTION
        # ----------------------------------------------------

        morning_brief_state["status"] = "RUNNING"
        morning_brief_state["result"] = None
        morning_brief_state["error"] = None
        morning_brief_state["started_at"] = (
            datetime.now(timezone.utc).isoformat()
        )
        morning_brief_state["completed_at"] = None

    # --------------------------------------------------------
    # START BACKGROUND WORKER
    # --------------------------------------------------------

    worker = threading.Thread(
        target=run_morning_brief,
        daemon=True,
        name="CreatorOS-Morning-Brief",
    )

    worker.start()

    return {
        "status": "STARTED",
        "message": (
            "CreatorOS COO has started preparing "
            "the morning brief."
        ),
        "started_at": morning_brief_state["started_at"],
    }


# ============================================================
# REFRESH MORNING BRIEF
# ============================================================

@app.post("/morning-brief/refresh")
def refresh_morning_brief():

    with morning_brief_lock:

        if morning_brief_state["status"] == "RUNNING":

            return {
                "status": "RUNNING",
                "message": (
                    "A morning brief is already being generated."
                ),
            }

        morning_brief_state["status"] = "RUNNING"
        morning_brief_state["result"] = None
        morning_brief_state["error"] = None
        morning_brief_state["started_at"] = (
            datetime.now(timezone.utc).isoformat()
        )
        morning_brief_state["completed_at"] = None

    worker = threading.Thread(
        target=run_morning_brief,
        daemon=True,
        name="CreatorOS-Morning-Brief-Refresh",
    )

    worker.start()

    return {
        "status": "STARTED",
        "message": "Morning brief refresh started.",
        "started_at": morning_brief_state["started_at"],
    }


# ============================================================
# APPROVE MISSION
# ============================================================

@app.post("/approve-mission")
def approve_mission(request: MissionApproval):

    # --------------------------------------------------------
    # OWNER REJECTED
    # --------------------------------------------------------

    if not request.approved:
        from app.database import Approval, SessionLocal

        db = SessionLocal()
        try:
            db.add(
                Approval(
                    resource_type="mission_opportunity",
                    resource_id=0,
                    status="rejected",
                    action_class="approval_required",
                    reason="CEO rejected opportunity.",
                    reviewed_by="owner",
                    reviewed_at=datetime.now(timezone.utc),
                )
            )
            db.commit()
        except Exception as db_err:
            print(f"[MISSION] Failed to record rejection approval: {db_err}")
            db.rollback()
        finally:
            db.close()

        return {
            "status": "REJECTED",
            "message": "Mission rejected by owner.",
            "next_step": "Review another opportunity.",
        }

    # --------------------------------------------------------
    # DEFAULT OPPORTUNITY
    # --------------------------------------------------------

    opportunity = request.opportunity or {
        "topic": (
            "Hyderabad gym trial-class enquiry campaign"
        ),
        "problem": (
            "Local gym prospects need a clear reason "
            "to enquire and an easy next step."
        ),
        "audience": [
            "Hyderabad gym owners",
            "beginners looking for a nearby class",
        ],
        "strategy": (
            "Create useful local-language short videos "
            "and route every CTA through an owner-approved "
            "follow-up."
        ),
        "recommended_content": [
            (
                "What to expect in your first gym "
                "trial class"
            ),
            (
                "Three questions to ask before joining "
                "a Hyderabad gym"
            ),
            (
                "A transparent introductory offer "
                "with a trial enquiry CTA"
            ),
        ],
        "product_idea": "",
    }

    # --------------------------------------------------------
    # SAFETY INSPECTION
    # --------------------------------------------------------

    from app.services.validation.opportunity_safety_gate import OpportunitySafetyGate
    safety_review = OpportunitySafetyGate().inspect(opportunity)

    # --------------------------------------------------------
    # EXECUTE MISSION
    # --------------------------------------------------------

    try:

        from app.agents.mission_planner import MissionPlanner
        from app.database import Approval, SessionLocal
        from app.services.mission_executor import MissionExecutor

        print()
        print("=" * 70)
        print("[MISSION] CREATING MISSION")
        print("=" * 70)

        planner = MissionPlanner()

        mission = planner.create_mission(
            opportunity
        )

        print(
            f"[MISSION] Created "
            f"{len(planner.task_manager.tasks)} tasks."
        )

        print("[MISSION] Starting Mission Executor...")

        execution_results = (
            MissionExecutor().execute_mission(
                planner.task_manager.tasks
            )
        )

        # ----------------------------------------------------
        # UPDATE TASK STATUSES
        # ----------------------------------------------------

        task_statuses = {
            result["task_id"]: result["status"]
            for result in execution_results
        }

        for task in mission["tasks"]:

            task["status"] = task_statuses.get(
                task["id"],
                task["status"],
            )

        # ----------------------------------------------------
        # DETERMINE MISSION STATUS
        # ----------------------------------------------------

        mission["execution_status"] = (
            "COMPLETED"
            if execution_results
            and all(
                result["status"] == "Completed"
                for result in execution_results
            )
            else "FAILED"
        )

        # ----------------------------------------------------
        # RECORD APPROVAL IN DB
        # ----------------------------------------------------

        db = SessionLocal()
        try:
            db.add(
                Approval(
                    resource_type="mission_opportunity",
                    resource_id=0,
                    status="approved",
                    action_class="approval_required",
                    reason=f"CEO approved opportunity: {opportunity.get('topic', 'Opportunity')}",
                    reviewed_by="owner",
                    reviewed_at=datetime.now(timezone.utc),
                )
            )
            db.commit()
        except Exception as db_err:
            print(f"[MISSION] Failed to record approval in database: {db_err}")
            db.rollback()
        finally:
            db.close()

        print(
            f"[MISSION] Execution status: "
            f"{mission['execution_status']}"
        )

        # ----------------------------------------------------
        # RETURN RESULT
        # ----------------------------------------------------

        return {
            "status": "APPROVED",
            "message": (
                "Mission executed. Generated artifacts "
                "remain approval-gated and require "
                "owner review."
            ),
            "mission": mission,
            "execution_results": execution_results,
            "safety_review": safety_review,
        }

    except Exception as error:

        print()
        print(
            "[MISSION] ERROR:",
            str(error),
        )
        print()

        raise HTTPException(
            status_code=503,
            detail=(
                "Mission execution could not be "
                "started safely."
            ),
        ) from error