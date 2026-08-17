from app.tasks.task_manager import TaskManager


class MissionPlanner:
    """
    CreatorOS Mission Planner

    Converts an approved business opportunity
    into executable tasks for AI employees.
    """

    def __init__(self):
        self.task_manager = TaskManager()

    def create_mission(self, opportunity):

        tasks = []

        # -------------------------------------------------
        # Extract opportunity information
        # -------------------------------------------------

        topic = opportunity.get(
            "topic",
            "Hyderabad Gym Trial-Class Enquiry Campaign"
        )

        problem = opportunity.get(
            "problem",
            ""
        )

        audience = opportunity.get(
            "audience",
            []
        )

        strategy = opportunity.get(
            "strategy",
            ""
        )

        product_idea = opportunity.get(
            "product_idea",
            ""
        )

        recommended_content = opportunity.get(
            "recommended_content",
            []
        )

        # -------------------------------------------------
        # CONTENT TASKS
        # -------------------------------------------------

        for index, content in enumerate(
            recommended_content[:3],
            start=1
        ):

            description = f"""
Create a claim-safe local-business content piece for a Hyderabad gym.

Topic:
{topic}

Content Idea:
{content}

Target Audience:
{", ".join(audience) if audience else "Gym owners and local adults in Hyderabad"}

Audience Problem:
{problem}

Business Strategy:
{strategy}

Requirements:
- Make the content engaging.
- Provide practical value.
- Keep it aligned with the gym/Hyderabad pilot.
- Optimize the opening for attention without clickbait.
- Include a clear trial-class enquiry call-to-action.
- Support English, Hinglish, Telugu, or Hindi when requested.
- Do not invent statistics or health claims.
- Do not guarantee fitness results, revenue, or enquiries.
- Mark the output for human review before publishing.
"""

            task = self.task_manager.create_task(
                title=f"Create Content #{index}",
                description=description.strip(),
                assigned_by="COO",
                assigned_to="Content Employee",
                priority="High"
            )

            tasks.append(task)

        # -------------------------------------------------
        # PRODUCT TASK
        # -------------------------------------------------

        if product_idea:

            product_description = f"""
Create a reusable campaign asset or operating playbook based on
the winning local-growth opportunity.

Opportunity:
{topic}

Audience:
{", ".join(audience) if audience else "Gym owners and local adults in Hyderabad"}

Audience Problem:
{problem}

Product Idea:
{product_idea}

Recommended Strategy:
{strategy}

The asset should:

- Solve a real gym-owner or local-customer problem.
- Be practical and actionable.
- Have a clear structure and owner-review checkpoint.
- Be suitable for a repeatable pilot workflow.
- Support trial-class enquiry generation.
- Avoid unsupported health, revenue, or performance guarantees.
"""

            task = self.task_manager.create_task(
                title="Create Digital Product",
                description=product_description.strip(),
                assigned_by="COO",
                assigned_to="Product Employee",
                priority="High"
            )

            tasks.append(task)

        # -------------------------------------------------
        # RETURN PLANNED MISSION
        # -------------------------------------------------

        return {
            "mission": topic,
            "status": "PLANNED",
            "opportunity": {
                "topic": topic,
                "problem": problem,
                "audience": audience,
                "product_idea": product_idea,
                "strategy": strategy
            },
            "tasks": [
                {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "assigned_by": task.assigned_by,
                    "assigned_to": task.assigned_to,
                    "priority": task.priority,
                    "status": task.status
                }
                for task in tasks
            ]
        }