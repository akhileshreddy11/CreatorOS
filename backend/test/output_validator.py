from app.services.validation.output_validator import OutputValidator


def main():

    print("\n===== CREATOROS OUTPUT VALIDATOR =====\n")

    validator = OutputValidator()

    # -----------------------------------------
    # TEST 1: GOOD CONTENT
    # -----------------------------------------

    good_content = {
        "hook": "Stop wasting time on repetitive content tasks.",
        "script": "Here are three practical ways to automate your workflow.",
        "caption": "Use automation to reduce repetitive work.",
        "cta": "Save this post for later.",
        "hashtags": [
            "#CreatorOS",
            "#AIAutomation"
        ]
    }

    result = validator.validate(good_content)

    print("TEST 1: GOOD CONTENT")
    print(result)

    assert result["valid"] is True

    # -----------------------------------------
    # TEST 2: UNSUPPORTED CLAIM
    # -----------------------------------------

    bad_content = {
        "hook": "Make $10,000 guaranteed with AI.",
        "script": "This guaranteed system will make you rich.",
        "caption": "Earn 500% more income.",
        "cta": "Buy now.",
        "hashtags": [
            "#AI"
        ]
    }

    result = validator.validate(bad_content)

    print("\nTEST 2: UNSUPPORTED CLAIM")
    print(result)

    assert result["valid"] is False

    # -----------------------------------------
    # TEST 3: VALID PRODUCT
    # -----------------------------------------

    product = {
        "product_name": "AI Creator OS",
        "tagline": "A practical growth operating system.",
        "description": (
            "A practical workflow system for creators "
            "and small businesses."
        ),
        "target_audience": [
            "Creators",
            "Freelancers"
        ],
        "product_structure": [
            {
                "module": "Content Planning",
                "description": "Plan and organize content.",
                "contents": [
                    "Content calendar",
                    "Content ideas",
                    "Approval checklist"
                ]
            }
        ],
        "prompt_pack": [
            {
                "name": "Content Idea Generator",
                "purpose": "Generate practical content ideas.",
                "prompt": "Create five useful content ideas."
            }
        ],
        "notion_workspace": {
            "pages": [
                "Content Calendar",
                "Campaign Tracker"
            ],
            "databases": [
                "Content Database",
                "Lead Database"
            ]
        },
        "automation_blueprints": [
            {
                "name": "Lead Follow-up",
                "purpose": "Prepare follow-up workflows.",
                "workflow": [
                    "Capture enquiry",
                    "Review lead",
                    "Prepare follow-up"
                ]
            }
        ],
        "pricing": {
            "recommended_price": "Pilot pricing",
            "premium_price": "Premium pricing",
            "reason": "Based on scope and implementation effort."
        },
        "marketing_angle": (
            "A practical operating system for organized growth."
        ),
        "launch_strategy": [
            "Prepare assets",
            "Review internally",
            "Launch pilot"
        ]
    }

    result = validator.validate(product)

    print("\nTEST 3: VALID PRODUCT")
    print(result)

    assert result["valid"] is True

    # -----------------------------------------
    # TEST 4: RAW CONTENT MUST FAIL
    # -----------------------------------------

    malformed_content = {
        "raw_content": "Some malformed AI output"
    }

    result = validator.validate(malformed_content)

    print("\nTEST 4: RAW CONTENT")
    print(result)

    assert result["valid"] is False

    # -----------------------------------------
    # TEST 5: ERROR RESPONSE MUST FAIL
    # -----------------------------------------

    error_response = {
        "status": "ERROR",
        "message": "Product Employee returned invalid JSON.",
        "raw_response": "not valid json"
    }

    result = validator.validate(error_response)

    print("\nTEST 5: ERROR RESPONSE")
    print(result)

    assert result["valid"] is False

    # -----------------------------------------
    # TEST 6: WRONG CONTENT TYPE
    # -----------------------------------------

    wrong_content_type = {
        "hook": 123,
        "script": "Valid script",
        "caption": "Valid caption",
        "cta": "Valid CTA",
        "hashtags": [
            "#CreatorOS"
        ]
    }

    result = validator.validate(wrong_content_type)

    print("\nTEST 6: WRONG CONTENT TYPE")
    print(result)

    assert result["valid"] is False

    # -----------------------------------------
    # TEST 7: UNKNOWN OUTPUT
    # -----------------------------------------

    unknown_output = {
        "random_field": "random value"
    }

    result = validator.validate(unknown_output)

    print("\nTEST 7: UNKNOWN OUTPUT")
    print(result)

    assert result["valid"] is False

    print("\n===== ALL VALIDATOR TESTS PASSED =====\n")


if __name__ == "__main__":
    main()