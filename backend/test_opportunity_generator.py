import json

from app.agents.opportunity_generator import OpportunityGenerator


def main():

    print("\n===== CREATOROS OPPORTUNITY GENERATOR =====\n")

    niche_data = {
        "best_niche": "AI-Enhanced Solopreneur Systems",
        "overall_score": 88,
        "reason": (
            "It occupies the sweet spot of high interest, "
            "massive utility, and easy productization of workflows."
        ),
        "niche_analysis": {
            "demand_score": 95,
            "reach_score": 90,
            "trend_score": 95,
            "competition_score": 40,
            "monetization_score": 90,
            "content_potential_score": 95,
            "product_potential_score": 90
        },
        "audience": [
            "Solopreneurs",
            "Freelancers",
            "Content Creators"
        ],
        "audience_problems": [
            "Overwhelmed by AI tool fatigue",
            "Difficulty scaling operations without hiring",
            "Inconsistent content creation workflow"
        ]
    }

    generator = OpportunityGenerator()

    result = generator.generate(niche_data)

    print(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False
        )
    )


if __name__ == "__main__":
    main()