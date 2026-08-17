"""Research local growth opportunities for the configured CreatorOS pilot."""

import json

from app.services.ai_brain import AIBrain


class NicheResearcher:
    """Find and compare lead-generation opportunities within the pilot niche.

    The initial workspace is deliberately narrow: gyms in Hyderabad.  The
    output keeps the legacy ranked-niches contract so the business-partner
    pipeline can continue to consume it, but the candidates are now campaign
    opportunities rather than unrelated creator-economy niches.
    """

    def __init__(self):
        self.brain = AIBrain()

    def research(self, audience="Gym owners and local adults in Hyderabad"):
        system_prompt = """
You are the Niche Researcher of CreatorOS, an AI business-intelligence
employee supporting a local-growth pilot.

The active pilot is for gyms in Hyderabad. Find and rank five practical
campaign opportunities that could help a gym generate more trial-class
enquiries through short-form content, local offers, and approval-gated
follow-up preparation.

Use the supplied audience and business context. Treat every score as a
strategic estimate, not live market data. Do not claim access to live social
analytics, invent search volumes, or guarantee reach, revenue, members,
health outcomes, or enquiries.

Return ONLY valid JSON, with no markdown or code fences, in exactly this
shape:
{
  "ranked_niches": [
    {
      "rank": 1,
      "niche": "...",
      "overall_score": 0,
      "scores": {
        "demand": 0,
        "reach": 0,
        "trend": 0,
        "competition": 0,
        "monetization": 0,
        "content_potential": 0,
        "product_potential": 0,
        "sustainability": 0
      },
      "audience": ["..."],
      "audience_problems": ["..."],
      "content_opportunities": ["..."],
      "product_opportunity": "...",
      "reason": "..."
    }
  ],
  "best_niche": {
    "niche": "...",
    "overall_score": 0,
    "reason": "...",
    "recommended_strategy": "..."
  }
}

Return exactly five candidates, ordered strongest to weakest. Use integer
scores from 0 to 100 and distinguish the candidates meaningfully. Keep
recommendations suitable for human review before any external send or
publication.
"""

        user_prompt = f"""
Research five campaign opportunities for the CreatorOS local-growth pilot.

Niche: gyms
City: Hyderabad
Primary KPI: trial-class enquiries
Offer: short videos, local offers, and approval-gated follow-up
Supported languages: English, Hinglish, Telugu, and Hindi
Target audience: {audience}

Prioritize opportunities that are useful for prospect audits, personalized
content drafts, local offers, response follow-up preparation, or appointment
conversion. Explain the audience problem and the content angle without
inventing performance data.

Return ONLY valid JSON.
"""

        response = self.brain.think(system_prompt, user_prompt)
        return self._parse_response(response)

    @staticmethod
    def _parse_response(response):
        if isinstance(response, dict):
            return response

        cleaned = str(response).strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        elif cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]

        try:
            return json.loads(cleaned.strip())
        except json.JSONDecodeError:
            return {
                "status": "FAILED",
                "reason": "AI returned invalid JSON.",
                "raw_response": response,
            }
