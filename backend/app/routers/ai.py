from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import Approval, ContentDraft, ErrorEvent, get_db
from app.schemas.prompt import PromptRequest, PromptResponse
from app.services.ai_brain import AIBrain
from app.services.structured_output import parse_json_object
from app.services.validation.output_validator import OutputValidator

router = APIRouter(prefix="/ai", tags=["AI"])


def _render_content(content: dict[str, Any]) -> str:
    sections = [
        ("Hook", content.get("hook")),
        ("Script", content.get("script")),
        ("Caption", content.get("caption")),
        ("Call to action", content.get("cta")),
    ]
    rendered = [f"{label}\n{value}" for label, value in sections if value]
    hashtags = content.get("hashtags")
    if hashtags:
        rendered.append("Hashtags\n" + " ".join(str(tag) for tag in hashtags))
    return "\n\n".join(rendered)


def _build_prompts(request: PromptRequest) -> tuple[str, str]:
    system_prompt = """
You are CreatorOS's local-business content strategist.
Create practical, claim-safe marketing content for a gym in a named city.
The goal is to encourage genuine trial-class enquiries, not to promise revenue,
reach, or guaranteed results. Do not invent testimonials, statistics, discounts,
or customer outcomes. Use the requested language naturally and return only JSON.
"""
    user_prompt = f"""
Create one {request.platform} asset for this operating brief.

Prompt: {request.prompt}
Niche: {request.niche}
City: {request.city}
Language: {request.language}
Length: {request.length}
Tone: {request.tone}
Objective: {request.objective}
Offer: {request.offer}

Return exactly this JSON shape:
{{
  "hook": "...",
  "script": "...",
  "caption": "...",
  "cta": "...",
  "hashtags": ["...", "..."]
}}
"""
    return system_prompt, user_prompt


@router.post("/generate", response_model=PromptResponse)
async def generate_content(request: PromptRequest, db: Session = Depends(get_db)):
    system_prompt, user_prompt = _build_prompts(request)

    try:
        raw_response = AIBrain().think(system_prompt, user_prompt)
        content = parse_json_object(raw_response)
        validation = OutputValidator().validate(content)
    except (ValueError, RuntimeError) as error:
        db.add(ErrorEvent(severity="warning", component="ai_generation", message=str(error)[:1500]))
        db.commit()
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(error)) from error
    except Exception as error:
        db.add(ErrorEvent(severity="error", component="ai_generation", message="Unexpected AI provider error: " + str(error)[:1200]))
        db.commit()
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="The AI provider did not complete the request.") from error

    if not validation.get("valid", False):
        db.add(ErrorEvent(
            severity="warning",
            component="ai_output_validation",
            message="Generated AI content failed schema/claim validation: " + "; ".join(validation.get("errors", []))[:1200],
        ))
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"message": "AI output failed CreatorOS validation.", "validation": validation},
        )

    draft = ContentDraft(
        title=str(content.get("hook") or "Untitled local campaign")[:180],
        prompt=request.prompt,
        platform=request.platform,
        language=request.language,
        content=content,
        validation=validation,
        status="needs_review",
        action_class="approval_required",
    )
    db.add(draft)
    db.flush()
    db.add(Approval(
        resource_type="content_draft",
        resource_id=draft.id,
        status="needs_review",
        action_class="approval_required",
        reason="AI-generated content passed validation but requires owner approval before publishing.",
    ))
    db.commit()
    db.refresh(draft)

    return PromptResponse(
        response=_render_content(content),
        content=content,
        validation=validation,
        approval_status="needs_review",
        action_class="approval_required",
        draft_id=draft.id,
    )
