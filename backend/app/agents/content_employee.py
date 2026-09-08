from app.services.ai_brain import AIBrain
from app.services.structured_output import parse_json_object


class ContentEmployee:
    """
    CreatorOS AI Employee #3

    Mission:
    Create claim-safe, local-business content
    from tasks assigned by the COO.
    """

    def __init__(self):
        self.brain = AIBrain()

    def create_content(self, task, feedback=None):

        system_prompt = """
You are the Content Employee of CreatorOS.

You are an AI employee, not a chatbot.

Your job is to create high-quality social media content
from the task assigned to you.

Create practical, engaging content for Hyderabad gyms
that helps generate trial-class enquiries.

IMPORTANT:
- Do not invent statistics.
- Do not make unsupported income claims.
- Do not claim guaranteed results.
- Avoid unsupported numerical performance claims.
- If a previous output was rejected by the validator,
  correct the specific problems identified in the feedback.

Return ONLY valid JSON.

The JSON must contain exactly:

{
"hook": "...",
"script": "...",
"caption": "...",
"cta": "...",
"hashtags": ["...", "...", "..."]
}
"""

        user_prompt = f"""
Create content for this task:

Title:
{task.title}

Description:
{task.description}

Platform:
Instagram

Target Audience:
Gym owners and local adults in Hyderabad considering a trial class.

Business context:
- Niche: gyms
- City: Hyderabad
- Primary outcome: trial-class enquiries
- Offer: short videos, local offers, and approval-gated follow-up

Make the content engaging, practical, locally relevant, and easy to understand.
Do not imply that a gym guarantees health, fitness, or medical outcomes.
"""

        # -----------------------------------------
        # VALIDATION FEEDBACK
        # -----------------------------------------

        if feedback:

            feedback_text = "\n".join(
                f"- {item}"
                for item in feedback
            )

            user_prompt += f"""

The previous version of this content failed validation.

Validator feedback:
{feedback_text}

Create a corrected version.

Do NOT repeat the problems identified above.
Return only the corrected JSON.
"""

        response = self.brain.think(
            system_prompt,
            user_prompt
        )

        return parse_json_object(response)