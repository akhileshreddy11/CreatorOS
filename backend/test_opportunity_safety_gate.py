from app.services.validation.opportunity_safety_gate import OpportunitySafetyGate


def test_safe_opportunity_passes_gate():
    gate = OpportunitySafetyGate()
    opportunity = {
        "topic": "3-Day Beginner Gym Onboarding Campaign",
        "problem": "Beginners in Hitech City feel intimidated by gym equipment and lack a clear routine.",
        "audience": ["Corporate tech workers", "Beginners"],
        "strategy": "Publish beginner tips and offer a complimentary coach-guided orientation.",
        "recommended_content": [
            "What to expect in your first workout session",
            "Top 3 beginner gym mistakes to avoid",
            "How our trainers help you set up machines properly",
        ],
        "product_idea": "7-Day Beginner Gym Starter Guide",
    }
    deliverables = ["3 Instagram Reels", "1 Onboarding Guide PDF", "1 Trial Enquiry Workflow"]

    result = gate.inspect(opportunity, deliverables)
    assert result["passed"] is True
    assert result["status"] == "SAFE"
    assert result["safety_score"] == 100
    assert len(result["flags"]) == 0


def test_physiotherapy_claim_is_flagged_as_needs_review():
    gate = OpportunitySafetyGate()
    opportunity = {
        "topic": "The Tech-Neck & Posture Correction Initiative",
        "problem": "Tech workers suffer from severe neck pain and spinal issues.",
        "audience": ["Software engineers"],
        "strategy": "3-Day Corrective Posture Trial with a 15-minute Physiotherapy assessment.",
        "recommended_content": [
            "Physiotherapist explains how to fix neck pain",
            "Clinical assessment for posture",
        ],
        "product_idea": "Physiotherapy Posture Program",
    }

    result = gate.inspect(opportunity)
    assert result["status"] == "NEEDS_REVIEW"
    assert result["safety_score"] < 100
    assert any("physiotherapy" in f["issue"].lower() or "medical" in f["issue"].lower() for f in result["flags"])


def test_guaranteed_outcome_is_flagged():
    gate = OpportunitySafetyGate()
    opportunity = {
        "topic": "Guaranteed 10kg Weight Loss in 30 Days",
        "problem": "Need quick fat loss.",
        "strategy": "Guaranteed weight loss program or 100% money back.",
    }

    result = gate.inspect(opportunity)
    assert result["status"] == "NEEDS_REVIEW"
    assert any("guarantee" in f["issue"].lower() for f in result["flags"])


def test_empty_opportunity_fails_safely():
    gate = OpportunitySafetyGate()
    result = gate.inspect(None)
    assert result["status"] == "NEEDS_REVIEW"
    assert result["passed"] is False
