import json

from app.services.ai_brain import AIBrain


class NicheHunter:
    """
    CreatorOS AI Employee - Niche Hunter

    Mission:
    Discover and rank local-growth campaign angles within the
    configured Hyderabad gym pilot.
    """

    def __init__(self):
        self.brain = AIBrain()

    def analyze(self, business_profile):

        system_prompt = """
You are the Niche Hunter of CreatorOS.

You are an AI business intelligence employee, not a chatbot.

Your mission is to discover the best campaign angles that CreatorOS
should test for Hyderabad gyms and trial-class enquiries.

Analyze niches strategically.

Evaluate each niche using:

1. Demand
2. Growth potential
3. Audience size
4. Engagement potential
5. Content potential
6. Monetization potential
7. Competition
8. CreatorOS business fit
9. Long-term sustainability

Do NOT simply choose the most popular niche.

Look for the best combination of:
- Clear gym-owner or local-customer demand
- Strong short-form content opportunities
- A useful local offer or follow-up angle
- Measurable trial-class enquiry potential
- Reasonable campaign effort and competition
- Safe, repeatable long-term operations

Score every niche from 0 to 100.

Calculate:

reach_score
monetization_score
competition_score
content_score
growth_score
overall_score

Return ONLY valid JSON.

Use exactly this structure:

{
    "analysis_date": "...",
    "market_summary": "...",
    "top_niches": [
        {
            "rank": 1,
            "niche": "...",
            "sub_niches": [
                "...",
                "...",
                "..."
            ],
            "reach_score": 0,
            "monetization_score": 0,
            "competition_score": 0,
            "content_score": 0,
            "growth_score": 0,
            "overall_score": 0,
            "target_audience": "...",
            "why_now": "...",
            "content_opportunities": [
                "...",
                "...",
                "..."
            ],
            "monetization_opportunities": [
                "...",
                "...",
                "..."
            ],
            "risks": [
                "...",
                "..."
            ]
        }
    ],
    "winner": {
        "niche": "...",
        "overall_score": 0,
        "reason": "...",
        "recommended_sub_niche": "...",
        "recommended_content_angle": "...",
        "recommended_product_angle": "..."
    }
}
"""

        user_prompt = f"""
Analyze the following CreatorOS business profile:

{json.dumps(business_profile, indent=2)}

CreatorOS wants to grow primarily through Instagram.

Find the best niches for:

- Maximum organic reach
- Strong engagement
- Useful short-form content
- Digital product opportunities
- Long-term business growth

Identify at least 5 promising niches.

Do not blindly assume AI is the best niche.
Compare AI with other potentially valuable niches.

Prioritize opportunities that fit the business profile.

Return ONLY valid JSON.
"""

        response = self.brain.think(
            system_prompt,
            user_prompt
        )

        try:
            return json.loads(response)

        except json.JSONDecodeError:

            cleaned = response.strip()

            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]

            if cleaned.startswith("```"):
                cleaned = cleaned[3:]

            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]

            cleaned = cleaned.strip()

            try:
                return json.loads(cleaned)

            except json.JSONDecodeError:
                return {
                    "status": "ERROR",
                    "message": "Niche Hunter returned invalid JSON.",
                    "raw_response": response
                }