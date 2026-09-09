from typing import Any

from pydantic import BaseModel, Field, field_validator


class PromptRequest(BaseModel):
    prompt: str = Field(min_length=3, max_length=5000)
    platform: str = Field(default="Instagram", max_length=50)
    length: str = Field(default="Medium", max_length=50)
    niche: str = Field(default="Gyms", max_length=120)
    city: str = Field(default="Hyderabad", max_length=120)
    language: str = Field(default="en", max_length=20)
    objective: str = Field(default="Generate trial-class enquiries", max_length=240)
    offer: str = Field(
        default="Short videos, local offers, and approval-gated follow-up",
        max_length=500,
    )
    tone: str = Field(default="Helpful and local", max_length=80)

    @field_validator("prompt", "platform", "length", "niche", "city", "language", "objective", "offer", "tone")
    @classmethod
    def strip_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("This field cannot be empty.")
        return value


class PromptResponse(BaseModel):
    response: str
    content: dict[str, Any]
    validation: dict[str, Any]
    approval_status: str = "needs_review"
    action_class: str = "approval_required"
    draft_id: int | None = None
