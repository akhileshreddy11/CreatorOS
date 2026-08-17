import json

from app.services.ai_brain import AIBrain


class OpportunityGenerator:
    """
    CreatorOS Opportunity Generator

    Converts a local-growth research result into multiple campaign opportunities.

    Responsibilities:
    - Generate content opportunities
    - Identify audience problems
    - Identify service and campaign opportunities
    - Identify reusable campaign-asset opportunities
    - Score opportunities
    - Select the strongest opportunity
    """

    def __init__(self):
        self.brain = AIBrain()

    def generate(self, niche_data):

        system_prompt = """
You are the Opportunity Generator of CreatorOS.

Your job is to convert local research into practical campaign
opportunities for gyms in Hyderabad.

CreatorOS wants to:

1. Help gyms generate trial-class enquiries
2. Create useful short-form content and local offers
3. Prepare personalized, approval-gated outreach
4. Track replies, leads, appointments, and KPI events
5. Build repeatable service delivery without bypassing human review

Analyze the winning niche carefully.

Generate multiple business opportunities.

Each opportunity must have:

- A clear topic
- A real audience problem
- Strong content potential
- Strong reach potential
- Service and campaign value
- A practical offer or campaign asset
- Recommended content and outreach ideas
- A realistic, approval-gated execution strategy

IMPORTANT:

- Do not claim access to live analytics.
- Do not invent real revenue figures.
- Do not guarantee income.
- Do not use fake statistics.
- Do not simply repeat the niche name.
- Focus on specific problems that can become content,
  products, and business systems.
- Prefer opportunities that can eventually be automated.

Score every opportunity from 0 to 100.

Higher scores mean better business opportunities.

Return ONLY valid JSON.

Do not use markdown.
Do not use ```json.
"""

        user_prompt = f"""
Analyze the following winning niche selected by CreatorOS.

WINNING NICHE:

{json.dumps(niche_data, indent=2)}

Generate 5 different business opportunities within this niche.

Rank them from strongest to weakest.

Prioritize:

- Audience demand
- Social media reach
- Trend potential
- Content potential
- Monetization
- Reusable campaign-asset potential
- Long-term sustainability
- Automation potential

Return exactly this JSON structure:

{{
    "niche": "...",

    "opportunities": [
        {{
            "rank": 1,
            "topic": "...",
            "problem": "...",
            "audience": [
                "...",
                "...",
                "..."
            ],
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
            "recommended_content": [
                "...",
                "...",
                "..."
            ],
            "product_idea": "...",
            "strategy": "..."
        }}
    ],

    "best_opportunity": {{
        "topic": "...",
        "overall_score": 0,
        "reason": "...",
        "product_idea": "...",
        "recommended_content": [
            "...",
            "...",
            "..."
        ]
    }}
}}

All scores must be integers between 0 and 100.
The best opportunity must be selected from the five opportunities.
"""

        response = self.brain.think(
            system_prompt,
            user_prompt
        )

        return self._parse_response(response)

    def _parse_response(self, response):

        if isinstance(response, dict):
            return response

        cleaned = response.strip()

        # Remove accidental markdown code fences
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]

        elif cleaned.startswith("```"):
            cleaned = cleaned[3:]

        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]

        cleaned = cleaned.strip()

        try:
            return json.loads(cleaned)

        except json.JSONDecodeError:

            return {
                "status": "FAILED",
                "reason": "AI returned invalid JSON.",
                "raw_response": response
            }