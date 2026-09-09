import pytest

from app.schemas.prompt import PromptRequest
from app.services.ai_brain import AIBrain
from app.services.validation.output_validator import OutputValidator


def test_ai_brain_requires_configuration(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    with pytest.raises(ValueError, match="GEMINI_API_KEY"):
        AIBrain()


def test_prompt_request_has_local_business_defaults():
    request = PromptRequest(prompt="Explain a beginner gym trial class")
    assert request.niche == "Gyms"
    assert request.city == "Hyderabad"
    assert request.objective == "Generate trial-class enquiries"


def test_validator_rejects_unsupported_guarantees():
    result = OutputValidator().validate(
        {
            "hook": "Guaranteed results for every gym",
            "script": "Try our class.",
            "caption": "Learn more.",
            "cta": "Message us.",
        }
    )
    assert result["valid"] is False
    assert result["errors"]
