import json
from pathlib import Path

from app.services.ai_brain import AIBrain


class TrendHunter:
    """
    AI Employee #2 - Trend Hunter

    Mission:
    Find useful local-growth opportunities for the active pilot.
    """

    def __init__(self):

        self.memory_path = (
            Path(__file__).parent.parent
            / "memory"
            / "business_profile.json"
        )

        self.business = self.load_business()

        self.brain = AIBrain()

    def load_business(self):

        with open(self.memory_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def analyze(self):

        system_prompt = """
You are the Trend Hunter of CreatorOS.

You are NOT a chatbot.

You are an AI employee.

Your responsibility is to identify strong business opportunities
for CreatorOS based on the business profile provided.

Think like a business strategist.

IMPORTANT:
- Do not claim you have live search data unless live data is provided.
- Do not invent exact search volumes or engagement statistics.
- Base your reasoning on the information available to you.
- - Prioritize opportunities that can help Hyderabad gyms generate
  trial-class enquiries through short videos, local offers, and
  approval-gated follow-up.
- Consider content potential, audience fit, operational effort, and KPI value.

Return ONLY valid JSON.
Do not use markdown.
Do not include ```json.
"""

        user_prompt = f"""
Business Profile:

{json.dumps(self.business, indent=2)}

Return JSON in exactly this format:

{{
    "topic": "...",
    "reason": "...",
    "confidence": 95,
    "recommended_content": [
        "...",
        "...",
        "..."
    ],
    "best_posting_time": "...",
    "product_idea": "..."
}}
"""

        response = self.brain.think(
            system_prompt,
            user_prompt
        )

        # Remove accidental markdown formatting
        response = response.strip()

        if response.startswith("```json"):
            response = response[7:]

        elif response.startswith("```"):
            response = response[3:]

        if response.endswith("```"):
            response = response[:-3]

        response = response.strip()

        # Convert JSON string into a real Python dictionary
        try:
            return json.loads(response)

        except json.JSONDecodeError:
            return {
                "error": "Trend Hunter returned invalid JSON",
                "raw_response": response
            }