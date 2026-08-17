import json

from app.agents.niche_hunter import NicheHunter


# CreatorOS business profile for testing
business_profile = {
    "business": {
        "name": "CreatorOS"
    },
    "goals": {
        "monthly_income": 100000,
        "primary_platform": "Instagram",
        "automation_level": "Maximum"
    },
    "audience": {
        "age": "18-35",
        "type": [
            "Creators",
            "Freelancers",
            "Students",
            "Solopreneurs"
        ]
    }
}


hunter = NicheHunter()

result = hunter.analyze(business_profile)

print("\n===== NICHE HUNTER RESULT =====\n")

print(json.dumps(result, indent=4))