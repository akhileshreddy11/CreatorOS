import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.database import init_db
from app.routers.ai import router as ai_router
from app.routers.operations import router as operations_router


init_db()

app = FastAPI(
    title="CreatorOS API",
    version="2.0.0",
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


class MissionApproval(BaseModel):
    approved: bool
    opportunity: dict | None = None


@app.get("/")
def root():
    return {
        "message": "CreatorOS API is running.",
        "status": "success",
        "product": "Approval-gated local-business lead generation",
    }


@app.get("/health")
def health():
    return {"status": "healthy", "database": "ready"}


@app.get("/morning-brief")
def morning_brief():
    try:
        from app.agents.business_partner import BusinessPartner

        return BusinessPartner().morning_brief()
    except (ValueError, RuntimeError) as error:
        raise HTTPException(status_code=503, detail=str(error)) from error


@app.post("/approve-mission")
def approve_mission(request: MissionApproval):
    if not request.approved:
        return {
            "status": "REJECTED",
            "message": "Mission rejected by owner.",
            "next_step": "Review another opportunity.",
        }

    opportunity = request.opportunity or {
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

    try:
        from app.agents.mission_planner import MissionPlanner

        planner = MissionPlanner()
        mission = planner.create_mission(opportunity)
        return {
            "status": "APPROVED",
            "message": "Mission planned. Individual content outputs remain approval-gated.",
            "mission": mission,
            "execution_results": [],
        }
    except Exception as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
