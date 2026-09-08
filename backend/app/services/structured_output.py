"""Helpers for parsing structured responses from AI employees."""

import json
from typing import Any


_ERROR_MESSAGE = "AI employee returned invalid JSON object output."


def parse_json_object(response: Any) -> dict:
    """
    Parse an AI response without inventing a fallback payload.

    A malformed response is returned as an explicit error-shaped dictionary so
    the normal OutputValidator path can reject it and the MissionExecutor can
    retry it with feedback.
    """

    if isinstance(response, dict):
        return response

    if not isinstance(response, str):
        return {
            "status": "ERROR",
            "message": _ERROR_MESSAGE,
            "raw_response": repr(response),
        }

    cleaned = response.strip()
    candidates = [cleaned]

    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        if lines and lines[0].strip().startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        candidates.append("\n".join(lines).strip())

    # Some providers add a short explanation around an otherwise valid JSON
    # object. Try the outermost object as a recovery path, but never synthesize
    # missing fields or accept a non-object JSON value.
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start >= 0 and end > start:
        candidates.append(cleaned[start : end + 1])

    for candidate in candidates:
        try:
            parsed = json.loads(candidate)
        except (TypeError, json.JSONDecodeError):
            continue

        if isinstance(parsed, dict):
            return parsed

    return {
        "status": "ERROR",
        "message": _ERROR_MESSAGE,
        "raw_response": response,
    }
