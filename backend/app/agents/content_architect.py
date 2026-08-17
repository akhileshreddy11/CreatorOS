"""Build a safe content brief before a draft is sent to an AI employee."""


class ContentArchitect:
    """Create a consistent local-business brief for downstream generators."""

    def build_brief(
        self,
        topic: str,
        niche: str = "Gyms",
        city: str = "Hyderabad",
        language: str = "en",
        objective: str = "Generate trial-class enquiries",
        offer: str = "Short videos, local offers, and approval-gated follow-up",
    ) -> dict:
        return {
            "topic": topic.strip(),
            "niche": niche.strip(),
            "city": city.strip(),
            "language": language.strip().lower(),
            "objective": objective.strip(),
            "offer": offer.strip(),
            "approval_status": "needs_review",
            "action_class": "approval_required",
            "constraints": [
                "Do not invent testimonials, statistics, or outcomes.",
                "Do not promise reach, revenue, or guaranteed results.",
                "Keep external publishing behind owner approval.",
            ],
        }
