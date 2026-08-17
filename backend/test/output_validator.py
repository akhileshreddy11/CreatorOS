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

    # -----------------------------------------
    # TEST 2: UNSUPPORTED CLAIM
    # -----------------------------------------

    bad_content = {
        "hook": "Make $10,000 guaranteed with AI.",
        "script": "This guaranteed system will make you rich.",
        "caption": "Earn 500% more income.",
        "cta": "Buy now."
    }

    result = validator.validate(bad_content)

    print("\nTEST 2: UNSUPPORTED CLAIM")
    print(result)

    # -----------------------------------------
    # TEST 3: PRODUCT
    # -----------------------------------------

    product = {
        "product_name": "AI Creator OS",
        "description": "A practical workflow system for creators.",
        "target_audience": [
            "Creators",
            "Freelancers"
        ],
        "product_structure": [
            {
                "module": "Content Planning",
                "description": "Plan and organize content."
            }
        ]
    }

    result = validator.validate(product)

    print("\nTEST 3: PRODUCT")
    print(result)


if __name__ == "__main__":
    main()