from app.agents.niche_ranking import NicheRanking


def test_niche_ranking_selects_highest_scoring_candidate():
    result = NicheRanking().rank(
        {
            "ranked_niches": [
                {"niche": "Generic creators", "overall_score": 62},
                {"niche": "Local gyms", "overall_score": 88},
            ]
        }
    )
    assert result["best_niche"]["niche"] == "Local gyms"
    assert result["ranked_niches"][0]["rank"] == 1
