import json
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import ContentDraft, ErrorEvent, get_db
from app.schemas.prompt import PromptRequest, PromptResponse
from app.services.ai_brain import AIBrain
from app.services.validation.output_validator import OutputValidator

router = APIRouter(prefix="/ai", tags=["AI"])


def _parse_json_response(raw_response: str) -> dict[str, Any] | None:
    cleaned = raw_response.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    elif cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    cleaned = cleaned.strip()

    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError:
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start < 0 or end <= start:
            return None
        try:
            parsed = json.loads(cleaned[start : end + 1])
        except json.JSONDecodeError:
            return None

    return parsed if isinstance(parsed, dict) else None


def _fallback_content(raw_response: str, request: PromptRequest) -> dict[str, Any]:
    return {
        "hook": request.prompt[:120],
        "script": raw_response.strip(),
        "caption": raw_response.strip(),
        "cta": f"Message us to learn more about {request.offer.lower()}.",
        "hashtags": ["#Hyderabad", "#GymMarketing", "#TrialClass"],
    }


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
        brain = AIBrain()
        raw_response = brain.think(system_prompt, user_prompt)
    except (ValueError, RuntimeError) as error:
        db.add(
            ErrorEvent(
                severity="warning",
                component="ai_generation",
                message=str(error),
            )
        )
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(error),
        ) from error
    except Exception as error:
        db.add(
            ErrorEvent(
                severity="error",
                component="ai_generation",
                message="Unexpected AI provider error: " + str(error),
            )
        )
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="The AI provider did not complete the request.",
        ) from error

    parsed_content = _parse_json_response(raw_response)
    required_fields = ("hook", "script", "caption", "cta", "hashtags")
    content = (
        parsed_content
        if parsed_content
        and all(isinstance(parsed_content.get(field), str) and parsed_content[field].strip() for field in required_fields[:4])
        and isinstance(parsed_content.get("hashtags"), list)
        else _fallback_content(raw_response, request)
    )
    validation = OutputValidator().validate(content)
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
