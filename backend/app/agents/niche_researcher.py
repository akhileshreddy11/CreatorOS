"""Research local growth opportunities for the configured CreatorOS pilot."""

from app.services.ai_brain import AIBrain
from app.services.structured_output import parse_json_object


class NicheResearcher:
    """Find and compare five campaign opportunities within the pilot niche."""

    def __init__(self):
        self.brain = AIBrain()

    def research(self, audience="Gym owners and local adults in Hyderabad"):
        system_prompt = """
You are the Niche Researcher of CreatorOS, an AI business-intelligence employee supporting a local-growth pilot.

The active pilot is for gyms in Hyderabad. Find and rank exactly five practical campaign opportunities that could help a gym generate more trial-class enquiries through short-form content, local offers, and approval-gated follow-up preparation.

Use the supplied audience and business context. Treat every score as a strategic estimate, not live market data. Do not claim access to live social analytics, invent search volumes, or guarantee reach, revenue, members, health outcomes, or enquiries.

Return ONLY valid JSON. Return exactly five candidates, ordered strongest to weakest, with integer scores from 0 to 100.
"""
        user_prompt = f"""
Research five campaign opportunities for the CreatorOS local-growth pilot.
Niche: gyms
City: Hyderabad
Primary KPI: trial-class enquiries
Offer: short videos, local offers, and approval-gated follow-up
Supported languages: English, Hinglish, Telugu, and Hindi
Target audience: {audience}

Return exactly this shape:
{{
  "ranked_niches": [
    {{
      "rank": 1,
      "niche": "...",
      "overall_score": 0,
      "scores": {{"demand": 0, "reach": 0, "trend": 0, "competition": 0, "monetization": 0, "content_potential": 0, "product_potential": 0, "sustainability": 0}},
      "audience": ["..."],
      "audience_problems": ["..."],
      "content_opportunities": ["..."],
      "product_opportunity": "...",
      "reason": "..."
    }}
  ],
  "best_niche": {{"niche": "...", "overall_score": 0, "reason": "...", "recommended_strategy": "..."}}
}}
"""
        return parse_json_object(self.brain.think(system_prompt, user_prompt))
