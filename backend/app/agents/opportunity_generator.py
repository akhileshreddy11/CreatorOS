import json

from app.services.ai_brain import AIBrain
from app.services.structured_output import parse_json_object


class OpportunityGenerator:
    """Convert local research into five ranked campaign opportunities."""

    def __init__(self):
        self.brain = AIBrain()

    def generate(self, niche_data):
        system_prompt = """
You are the Opportunity Generator of CreatorOS. Convert local research into practical campaign opportunities for gyms in Hyderabad.

Generate exactly five distinct opportunities. Each must identify a real audience problem, content potential, reach potential, monetization/service value, reusable campaign-asset potential, sustainability, and automation potential. Scores are strategic estimates from 0 to 100, not live analytics. Do not invent revenue, statistics, testimonials, or guarantees. The best_opportunity must be one of the five opportunities. Return only JSON.
"""
        user_prompt = f"""
Winning niche:
{json.dumps(niche_data, indent=2)}

Return exactly:
{{
  "niche": "...",
  "opportunities": [
    {{
      "rank": 1,
      "topic": "...",
      "problem": "...",
      "audience": ["..."],
      "demand_score": 0,
      "reach_score": 0,
      "trend_score": 0,
      "content_score": 0,
      "monetization_score": 0,
      "product_score": 0,
      "sustainability_score": 0,
      "automation_score": 0,
      "overall_score": 0,
      "reason": "...",
      "recommended_content": ["..."],
      "product_idea": "...",
      "strategy": "..."
    }}
  ],
  "best_opportunity": {{"topic": "...", "overall_score": 0, "reason": "...", "product_idea": "...", "recommended_content": ["..."]}}
}}

Return exactly five opportunities, ranked strongest to weakest. All scores must be integers 0-100.
"""
        return parse_json_object(self.brain.think(system_prompt, user_prompt))
