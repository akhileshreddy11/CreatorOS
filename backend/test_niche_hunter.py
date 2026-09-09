"""Manual Niche Hunter smoke test; kept out of deterministic pytest collection."""

import json

from app.agents.niche_hunter import NicheHunter


business_profile = {
    "business": {"name": "CreatorOS"},
    "goals": {
        "monthly_income": 100000,
        "primary_platform": "Instagram",
        "automation_level": "Maximum",
    },
    "audience": {
        "age": "18-35",
        "type": ["Creators", "Freelancers", "Students", "Solopreneurs"],
    },
}


def main():
    result = NicheHunter().analyze(business_profile)
    print("\n===== NICHE HUNTER RESULT =====\n")
    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()
