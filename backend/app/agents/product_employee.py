from app.services.ai_brain import AIBrain
from app.services.structured_output import parse_json_object


class ProductEmployee:
    """
    CreatorOS AI Employee #4

    Mission:
    Create reusable campaign assets and operating playbooks
    from tasks assigned to the COO.
    """

    def __init__(self):
        self.brain = AIBrain()

    def create_product(self, task, feedback=None):

        system_prompt = """
You are the Product Employee of CreatorOS.

You are an AI employee, not a chatbot.

Your job is to design high-quality campaign assets and operating
playbooks from tasks assigned to you by the COO.

CreatorOS focuses on approval-gated local growth for gyms in Hyderabad.
Create assets for gym owners and local adults considering a trial class.

Assets should be practical, useful, easy to understand, and ready for
human review before they are sent, published, or used in an external
workflow.

The product should contain real, actionable material,
not vague descriptions.

IMPORTANT:
- Do not invent statistics.
- Do not make unsupported income claims.
- Do not promise guaranteed results.
- Avoid unsupported numerical performance claims.
- Use realistic, defensible product descriptions.
- If a previous output was rejected by the validator,
  correct the specific problems identified in the feedback.

Return ONLY valid JSON.

Use exactly this structure:

{
"product_name": "...",
"tagline": "...",
"description": "...",
"target_audience": [
"...",
"...",
"..."
],
"product_structure": [
{
"module": "...",
"description": "...",
"contents": [
"...",
"...",
"..."
]
}
],
"prompt_pack": [
{
"name": "...",
"purpose": "...",
"prompt": "..."
}
],
"notion_workspace": {
"pages": [
"...",
"...",
"..."
],
"databases": [
"...",
"...",
"..."
]
},
"automation_blueprints": [
{
"name": "...",
"purpose": "...",
"workflow": [
"...",
"...",
"..."
]
}
],
"pricing": {
"recommended_price": "...",
"premium_price": "...",
"reason": "..."
},
"marketing_angle": "...",
"launch_strategy": [
"...",
"...",
"..."
]
}
"""

        user_prompt = f"""
Create a complete reusable campaign asset or operating playbook based on this task.

TASK TITLE:
{task.title}

TASK DESCRIPTION:
{task.description}

CREATOROS BUSINESS:
Approval-gated local growth operations for gyms in Hyderabad.
Primary KPI: trial-class enquiries.
Offer: short videos, local offers, and follow-up preparation.

PRIMARY PLATFORM:
Instagram

The asset or playbook should be realistic enough that CreatorOS
could actually use it to support a gym pilot.

Make the product:

- Practical
- Valuable
- Beginner-friendly
- Professional
- Easy to package for a gym pilot
- Easy to review and hand off to the owner
- Suitable for Instagram, WhatsApp preparation, or internal tracking

Include useful content prompts, audit fields, approval checkpoints,
follow-up workflows, and an implementation strategy.

Do not include unsupported statistics or guaranteed outcomes.

Return ONLY valid JSON.
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

The previous product output failed validation.

Validator feedback:
{feedback_text}

Create a corrected version.

Do NOT repeat the problems identified above.
Return only the corrected JSON.
"""

        # -----------------------------------------
        # GENERATE PRODUCT
        # -----------------------------------------

        response = self.brain.think(
            system_prompt,
            user_prompt
        )

        # -----------------------------------------
        # PARSE JSON
        # -----------------------------------------

        return parse_json_object(response)