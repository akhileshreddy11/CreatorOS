"""Persistence primitives for the CreatorOS operating dashboard."""

from __future__ import annotations

import os
from datetime import date, datetime
from typing import Generator

from dotenv import load_dotenv
from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, Integer, JSON, String, Text, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

load_dotenv()


DATABASE_URL = os.getenv("CREATOROS_DATABASE_URL", "sqlite:///./creatoros.db")

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class BusinessProfile(Base):
    __tablename__ = "business_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    niche: Mapped[str] = mapped_column(String(120), nullable=False)
    city: Mapped[str] = mapped_column(String(120), nullable=False)
    primary_language: Mapped[str] = mapped_column(String(40), default="en", nullable=False)
    supported_languages: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    offer: Mapped[str] = mapped_column(Text, nullable=False)
    primary_kpi: Mapped[str] = mapped_column(String(120), default="trial_class_enquiries", nullable=False)
    monthly_targets: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    approval_policy: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class Prospect(Base):
    __tablename__ = "prospects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    business_name: Mapped[str] = mapped_column(String(160), nullable=False)
    category: Mapped[str] = mapped_column(String(120), default="Gym", nullable=False)
    city: Mapped[str] = mapped_column(String(120), default="Hyderabad", nullable=False)
    contact_name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    contact_channel: Mapped[str] = mapped_column(String(40), default="instagram", nullable=False)
    contact_handle: Mapped[str | None] = mapped_column(String(160), nullable=True)
    audit_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(40), default="new", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class Outreach(Base):
    __tablename__ = "outreach"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    prospect_id: Mapped[int] = mapped_column(ForeignKey("prospects.id"), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    channel: Mapped[str] = mapped_column(String(40), default="instagram", nullable=False)
    status: Mapped[str] = mapped_column(String(40), default="draft", nullable=False)
    approval_status: Mapped[str] = mapped_column(String(40), default="needs_review", nullable=False)
    action_class: Mapped[str] = mapped_column(String(40), default="approval_required", nullable=False)
    response_status: Mapped[str] = mapped_column(String(40), default="not_contacted", nullable=False)
    follow_up_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    sent_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    prospect_id: Mapped[int | None] = mapped_column(ForeignKey("prospects.id"), nullable=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    source: Mapped[str] = mapped_column(String(80), default="manual", nullable=False)
    status: Mapped[str] = mapped_column(String(40), default="new", nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class Appointment(Base):
    __tablename__ = "appointments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lead_id: Mapped[int] = mapped_column(ForeignKey("leads.id"), nullable=False)
    scheduled_for: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[str] = mapped_column(String(40), default="scheduled", nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class ContentDraft(Base):
    __tablename__ = "content_drafts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(180), nullable=False)
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    platform: Mapped[str] = mapped_column(String(50), default="Instagram", nullable=False)
    language: Mapped[str] = mapped_column(String(40), default="en", nullable=False)
    content: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    validation: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    status: Mapped[str] = mapped_column(String(40), default="needs_review", nullable=False)
    action_class: Mapped[str] = mapped_column(String(40), default="approval_required", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class Approval(Base):
    __tablename__ = "approvals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    resource_type: Mapped[str] = mapped_column(String(50), nullable=False)
    resource_id: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(40), default="needs_review", nullable=False)
    action_class: Mapped[str] = mapped_column(String(40), default="approval_required", nullable=False)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    reviewed_by: Mapped[str | None] = mapped_column(String(120), nullable=True)
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class KPIEvent(Base):
    __tablename__ = "kpi_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    metric: Mapped[str] = mapped_column(String(100), nullable=False)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    source: Mapped[str] = mapped_column(String(80), default="manual", nullable=False)
    event_date: Mapped[date] = mapped_column(Date, default=date.today, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class ErrorEvent(Base):
    __tablename__ = "error_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    severity: Mapped[str] = mapped_column(String(20), default="warning", nullable=False)
    component: Mapped[str] = mapped_column(String(100), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    resolved: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        profile = db.scalar(select(BusinessProfile).limit(1))
        if profile is None:
            db.add(
                BusinessProfile(
                    name="CreatorOS",
                    niche="Gyms",
                    city="Hyderabad",
                    primary_language="en",
                    supported_languages=["en", "te", "hi"],
                    offer="Short videos, local offers, and approval-gated follow-up to generate more trial-class enquiries.",
                    primary_kpi="trial_class_enquiries",
                    monthly_targets={"month_1": 1, "month_2": "2-3", "month_3_plus": "4-6"},
                    approval_policy={
                        "draft_generation": "automatic",
                        "publishing": "approval_required",
                        "outreach_send": "approval_required",
                        "payments_contracts_deletion": "human_only",
                    },
                )
            )
            db.commit()
    finally:
        db.close()
