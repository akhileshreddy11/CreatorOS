from app.services.validation.output_validator import OutputValidator


validator = OutputValidator()


def good_content():
    return {
        "hook": "Stop wasting time on repetitive content tasks.",
        "script": "Here are practical ways to organize your workflow.",
        "caption": "Use automation to reduce repetitive work.",
        "cta": "Save this post for later.",
        "hashtags": ["#CreatorOS", "#AIAutomation"],
    }


def valid_product():
    return {
        "product_name": "AI Creator OS",
        "tagline": "A practical growth operating system.",
        "description": "A practical workflow system for creators and small businesses.",
        "target_audience": ["Creators", "Freelancers"],
        "product_structure": [
            {
                "module": "Content Planning",
                "description": "Plan and organize content.",
                "contents": ["Content calendar", "Approval checklist"],
            }
        ],
        "prompt_pack": [
            {
                "name": "Content Idea Generator",
                "purpose": "Generate practical content ideas.",
                "prompt": "Create five useful content ideas.",
            }
        ],
        "notion_workspace": {
            "pages": ["Content Calendar"],
            "databases": ["Content Database"],
        },
        "automation_blueprints": [
            {
                "name": "Lead Follow-up",
                "purpose": "Prepare follow-up workflows.",
                "workflow": ["Capture enquiry", "Review lead", "Prepare follow-up"],
            }
        ],
        "pricing": {
            "recommended_price": "Pilot pricing",
            "premium_price": "Premium pricing",
            "reason": "Based on scope and implementation effort.",
        },
        "marketing_angle": "A practical operating system for organized growth.",
        "launch_strategy": ["Prepare assets", "Review internally", "Launch pilot"],
    }


def test_good_content_is_approved():
    result = validator.validate(good_content())
    assert result["valid"] is True
    assert result["status"] == "APPROVED"


def test_unsupported_claim_is_rejected():
    result = validator.validate(
        {
            "hook": "Make $10,000 guaranteed with AI.",
            "script": "This guaranteed system will make you rich.",
            "caption": "Guaranteed results.",
            "cta": "Buy now.",
            "hashtags": ["#AI"],
        }
    )
    assert result["valid"] is False
    assert result["status"] == "NEEDS_REVIEW"


def test_valid_product_is_approved():
    result = validator.validate(valid_product())
    assert result["valid"] is True


def test_raw_content_is_rejected():
    result = validator.validate({"raw_content": "Malformed AI output"})
    assert result["valid"] is False


def test_error_response_is_rejected():
    result = validator.validate(
        {
            "status": "ERROR",
            "message": "Invalid JSON",
            "raw_response": "not valid json",
        }
    )
    assert result["valid"] is False


def test_wrong_content_field_type_is_rejected():
    result = validator.validate(
        {
            "hook": 123,
            "script": "Valid script",
            "caption": "Valid caption",
            "cta": "Valid CTA",
            "hashtags": ["#CreatorOS"],
        }
    )
    assert result["valid"] is False


def test_unknown_schema_is_rejected():
    result = validator.validate({"random_field": "random value"})
    assert result["valid"] is False
