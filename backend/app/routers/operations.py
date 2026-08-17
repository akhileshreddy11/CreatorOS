from __future__ import annotations

from datetime import datetime
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import (
    Appointment,
    Approval,
    BusinessProfile,
    ContentDraft,
    ErrorEvent,
    KPIEvent,
    Lead,
    Outreach,
    Prospect,
    get_db,
)

router = APIRouter(tags=["Operations"])


class ProspectCreate(BaseModel):
    business_name: str = Field(min_length=2, max_length=160)
    category: str = "Gym"
    city: str = "Hyderabad"
    contact_name: str | None = None
    contact_channel: str = "instagram"
    contact_handle: str | None = None
    audit_summary: str | None = None


class OutreachCreate(BaseModel):
    message: str = Field(min_length=10, max_length=5000)
    channel: str = "instagram"
    follow_up_at: datetime | None = None


class OutreachResponseUpdate(BaseModel):
    response_status: str = Field(min_length=2, max_length=40)


class LeadCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    prospect_id: int | None = None
    source: str = "manual"
    status: str = "new"
    notes: str | None = None


class LeadStatusUpdate(BaseModel):
    status: str = Field(min_length=2, max_length=40)
    notes: str | None = None


class AppointmentCreate(BaseModel):
    lead_id: int
    scheduled_for: datetime
    status: str = "scheduled"
    notes: str | None = None


class KPIEventCreate(BaseModel):
    metric: str = Field(min_length=2, max_length=100)
    value: float = Field(ge=0)
    source: str = "manual"
    notes: str | None = None


def _profile_dict(profile: BusinessProfile) -> dict[str, Any]:
    return {
        "id": profile.id,
        "name": profile.name,
        "niche": profile.niche,
        "city": profile.city,
        "primary_language": profile.primary_language,
        "supported_languages": profile.supported_languages,
        "offer": profile.offer,
        "primary_kpi": profile.primary_kpi,
        "monthly_targets": profile.monthly_targets,
        "approval_policy": profile.approval_policy,
    }


def _prospect_dict(prospect: Prospect) -> dict[str, Any]:
    return {
        "id": prospect.id,
        "business_name": prospect.business_name,
        "category": prospect.category,
        "city": prospect.city,
        "contact_name": prospect.contact_name,
        "contact_channel": prospect.contact_channel,
        "contact_handle": prospect.contact_handle,
        "audit_summary": prospect.audit_summary,
        "status": prospect.status,
        "created_at": prospect.created_at,
    }


def _outreach_dict(item: Outreach) -> dict[str, Any]:
    return {
        "id": item.id,
        "prospect_id": item.prospect_id,
        "message": item.message,
        "channel": item.channel,
        "status": item.status,
        "approval_status": item.approval_status,
        "action_class": item.action_class,
        "response_status": item.response_status,
        "follow_up_at": item.follow_up_at,
        "sent_at": item.sent_at,
        "created_at": item.created_at,
    }


def _lead_dict(lead: Lead) -> dict[str, Any]:
    return {
        "id": lead.id,
        "prospect_id": lead.prospect_id,
        "name": lead.name,
        "source": lead.source,
        "status": lead.status,
        "notes": lead.notes,
        "created_at": lead.created_at,
        "updated_at": lead.updated_at,
    }


def _draft_dict(draft: ContentDraft) -> dict[str, Any]:
    return {
        "id": draft.id,
        "title": draft.title,
        "prompt": draft.prompt,
        "platform": draft.platform,
        "language": draft.language,
        "content": draft.content,
        "validation": draft.validation,
        "status": draft.status,
        "action_class": draft.action_class,
        "created_at": draft.created_at,
        "updated_at": draft.updated_at,
    }


@router.get("/business-profile")
def get_business_profile(db: Session = Depends(get_db)):
    profile = db.scalar(select(BusinessProfile).limit(1))
    if profile is None:
        raise HTTPException(status_code=404, detail="Business profile is not configured.")
    return _profile_dict(profile)


@router.get("/dashboard/summary")
def dashboard_summary(db: Session = Depends(get_db)):
    profile = db.scalar(select(BusinessProfile).limit(1))
    prospect_total = db.scalar(select(func.count(Prospect.id))) or 0
    contacted = db.scalar(select(func.count(Outreach.id)).where(Outreach.status == "sent")) or 0
    replies = db.scalar(
        select(func.count(Outreach.id)).where(Outreach.response_status.not_in(["not_contacted", "no_response"]))
    ) or 0
    qualified = db.scalar(select(func.count(Lead.id)).where(Lead.status.in_(["qualified", "trial_enquiry"]))) or 0
    appointments = db.scalar(select(func.count(Appointment.id)).where(Appointment.status != "cancelled")) or 0
    trial_enquiries = db.scalar(
        select(func.coalesce(func.sum(KPIEvent.value), 0)).where(KPIEvent.metric == "trial_class_enquiries")
    ) or 0
    pending_approvals = (
        (db.scalar(select(func.count(ContentDraft.id)).where(ContentDraft.status == "needs_review")) or 0)
        + (db.scalar(select(func.count(Outreach.id)).where(Outreach.approval_status == "needs_review")) or 0)
    )
    open_errors = db.scalar(select(func.count(ErrorEvent.id)).where(ErrorEvent.resolved.is_(False))) or 0

    return {
        "profile": _profile_dict(profile) if profile else None,
        "metrics": {
            "prospects": prospect_total,
            "contacted": contacted,
            "replies": replies,
            "qualified_leads": qualified,
            "appointments": appointments,
            "trial_class_enquiries": trial_enquiries,
            "pending_approvals": pending_approvals,
            "open_errors": open_errors,
        },
        "conversion_rate": round((qualified / contacted) * 100, 1) if contacted else 0,
        "safety": {
            "external_sends_require_approval": True,
            "payments_contracts_and_deletion_require_human": True,
        },
    }


@router.get("/prospects")
def list_prospects(db: Session = Depends(get_db)):
    prospects = db.scalars(select(Prospect).order_by(Prospect.created_at.desc())).all()
    return [_prospect_dict(prospect) for prospect in prospects]


@router.post("/prospects", status_code=status.HTTP_201_CREATED)
def create_prospect(request: ProspectCreate, db: Session = Depends(get_db)):
    prospect = Prospect(**request.model_dump())
    db.add(prospect)
    db.commit()
    db.refresh(prospect)
    return _prospect_dict(prospect)


@router.post("/prospects/{prospect_id}/outreach", status_code=status.HTTP_201_CREATED)
def create_outreach(prospect_id: int, request: OutreachCreate, db: Session = Depends(get_db)):
    prospect = db.get(Prospect, prospect_id)
    if prospect is None:
        raise HTTPException(status_code=404, detail="Prospect not found.")
    outreach = Outreach(prospect_id=prospect_id, **request.model_dump())
    db.add(outreach)
    db.commit()
    db.refresh(outreach)
    return _outreach_dict(outreach)


@router.get("/outreach")
def list_outreach(db: Session = Depends(get_db)):
    items = db.scalars(select(Outreach).order_by(Outreach.created_at.desc())).all()
    return [_outreach_dict(item) for item in items]


@router.post("/outreach/{outreach_id}/approve")
def approve_outreach(outreach_id: int, db: Session = Depends(get_db)):
    outreach = db.get(Outreach, outreach_id)
    if outreach is None:
        raise HTTPException(status_code=404, detail="Outreach draft not found.")
    if outreach.approval_status not in {"needs_review", "revision_requested"}:
        raise HTTPException(status_code=409, detail="This outreach item is not awaiting approval.")
    outreach.approval_status = "approved"
    outreach.status = "approved"
    db.add(Approval(resource_type="outreach", resource_id=outreach.id, status="approved", action_class="approval_required", reviewed_by="owner", reviewed_at=datetime.utcnow()))
    db.commit()
    db.refresh(outreach)
    return _outreach_dict(outreach)


@router.post("/outreach/{outreach_id}/record-send")
def record_outreach_send(outreach_id: int, db: Session = Depends(get_db)):
    outreach = db.get(Outreach, outreach_id)
    if outreach is None:
        raise HTTPException(status_code=404, detail="Outreach draft not found.")
    if outreach.approval_status != "approved":
        raise HTTPException(status_code=409, detail="Owner approval is required before recording an external send.")
    outreach.status = "sent"
    outreach.sent_at = datetime.utcnow()
    db.commit()
    db.refresh(outreach)
    return {"message": "Send recorded. CreatorOS did not send an external message.", "outreach": _outreach_dict(outreach)}


@router.post("/outreach/{outreach_id}/response")
def record_outreach_response(outreach_id: int, request: OutreachResponseUpdate, db: Session = Depends(get_db)):
    outreach = db.get(Outreach, outreach_id)
    if outreach is None:
        raise HTTPException(status_code=404, detail="Outreach draft not found.")
    outreach.response_status = request.response_status
    db.commit()
    db.refresh(outreach)
    return _outreach_dict(outreach)


@router.get("/leads")
def list_leads(db: Session = Depends(get_db)):
    leads = db.scalars(select(Lead).order_by(Lead.created_at.desc())).all()
    return [_lead_dict(lead) for lead in leads]


@router.post("/leads", status_code=status.HTTP_201_CREATED)
def create_lead(request: LeadCreate, db: Session = Depends(get_db)):
    if request.prospect_id is not None and db.get(Prospect, request.prospect_id) is None:
        raise HTTPException(status_code=404, detail="Prospect not found.")
    lead = Lead(**request.model_dump())
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return _lead_dict(lead)


@router.post("/leads/{lead_id}/status")
def update_lead_status(lead_id: int, request: LeadStatusUpdate, db: Session = Depends(get_db)):
    lead = db.get(Lead, lead_id)
    if lead is None:
        raise HTTPException(status_code=404, detail="Lead not found.")
    lead.status = request.status
    if request.notes is not None:
        lead.notes = request.notes
    db.commit()
    db.refresh(lead)
    return _lead_dict(lead)


@router.get("/appointments")
def list_appointments(db: Session = Depends(get_db)):
    appointments = db.scalars(select(Appointment).order_by(Appointment.scheduled_for)).all()
    return [
        {
            "id": appointment.id,
            "lead_id": appointment.lead_id,
            "scheduled_for": appointment.scheduled_for,
            "status": appointment.status,
            "notes": appointment.notes,
        }
        for appointment in appointments
    ]


@router.post("/appointments", status_code=status.HTTP_201_CREATED)
def create_appointment(request: AppointmentCreate, db: Session = Depends(get_db)):
    if db.get(Lead, request.lead_id) is None:
        raise HTTPException(status_code=404, detail="Lead not found.")
    appointment = Appointment(**request.model_dump())
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return {
        "id": appointment.id,
        "lead_id": appointment.lead_id,
        "scheduled_for": appointment.scheduled_for,
        "status": appointment.status,
        "notes": appointment.notes,
    }


@router.get("/drafts")
def list_drafts(db: Session = Depends(get_db)):
    drafts = db.scalars(select(ContentDraft).order_by(ContentDraft.created_at.desc())).all()
    return [_draft_dict(draft) for draft in drafts]


@router.post("/drafts/{draft_id}/approve")
def approve_draft(draft_id: int, db: Session = Depends(get_db)):
    draft = db.get(ContentDraft, draft_id)
    if draft is None:
        raise HTTPException(status_code=404, detail="Draft not found.")
    if draft.status not in {"needs_review", "revision_requested"}:
        raise HTTPException(status_code=409, detail="This draft is not awaiting approval.")
    if not draft.validation.get("valid", False):
        raise HTTPException(
            status_code=409,
            detail="This draft failed claim-safety validation and needs revision before approval.",
        )
    draft.status = "approved"
    db.add(Approval(resource_type="content_draft", resource_id=draft.id, status="approved", action_class="approval_required", reviewed_by="owner", reviewed_at=datetime.utcnow()))
    db.commit()
    db.refresh(draft)
    return _draft_dict(draft)


@router.post("/drafts/{draft_id}/reject")
def reject_draft(draft_id: int, db: Session = Depends(get_db)):
    draft = db.get(ContentDraft, draft_id)
    if draft is None:
        raise HTTPException(status_code=404, detail="Draft not found.")
    if draft.status not in {"needs_review", "revision_requested"}:
        raise HTTPException(status_code=409, detail="This draft is not awaiting review.")
    draft.status = "rejected"
    db.add(Approval(resource_type="content_draft", resource_id=draft.id, status="rejected", action_class="approval_required", reviewed_by="owner", reviewed_at=datetime.utcnow()))
    db.commit()
    db.refresh(draft)
    return _draft_dict(draft)


@router.post("/kpi-events", status_code=status.HTTP_201_CREATED)
def create_kpi_event(request: KPIEventCreate, db: Session = Depends(get_db)):
    event = KPIEvent(**request.model_dump())
    db.add(event)
    db.commit()
    db.refresh(event)
    return {
        "id": event.id,
        "metric": event.metric,
        "value": event.value,
        "source": event.source,
        "event_date": event.event_date,
        "notes": event.notes,
    }


@router.get("/errors")
def list_errors(db: Session = Depends(get_db)):
    errors = db.scalars(select(ErrorEvent).order_by(ErrorEvent.created_at.desc()).limit(50)).all()
    return [
        {
            "id": item.id,
            "severity": item.severity,
            "component": item.component,
            "message": item.message,
            "resolved": item.resolved,
            "created_at": item.created_at,
        }
        for item in errors
    ]


@router.get("/trends")
def list_trends():
    return [
        {
            "title": "Trial-class transformation stories",
            "angle": "Show a clear first-session experience without promising an outcome.",
            "status": "idea",
        },
        {
            "title": "Hyderabad gym decision guide",
            "angle": "Answer local questions about timing, beginner comfort, and class formats.",
            "status": "idea",
        },
        {
            "title": "Offer-led Reel experiments",
            "angle": "Test one transparent introductory offer with an approval-gated CTA.",
            "status": "idea",
        },
    ]
