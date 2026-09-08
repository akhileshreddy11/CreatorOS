from app.tasks.task_manager import TaskManager


class MissionPlanner:
    """Convert an approved opportunity into an executable task graph."""

    def __init__(self):
        self.task_manager = TaskManager()

    def create_mission(self, opportunity):
        topic = opportunity.get("topic", "Hyderabad Gym Trial-Class Enquiry Campaign")
        problem = opportunity.get("problem", "")
        audience = opportunity.get("audience", [])
        strategy = opportunity.get("strategy", "")
        product_idea = opportunity.get("product_idea", "")
        recommended_content = opportunity.get("recommended_content", [])
        tasks = []

        for index, content in enumerate(recommended_content[:3], start=1):
            task = self.task_manager.create_task(
                title=f"Create Content #{index}",
                description=f"""
Create a claim-safe local-business content piece for a Hyderabad gym.
Topic: {topic}
Content idea: {content}
Target audience: {', '.join(audience) if audience else 'Gym owners and local adults in Hyderabad'}
Audience problem: {problem}
Business strategy: {strategy}
Requirements: engaging and practical; optimize the opening without clickbait; include a clear trial-class enquiry CTA; support English, Hinglish, Telugu, or Hindi when requested; do not invent statistics, testimonials, health claims, revenue, or guaranteed outcomes; mark for human review before publishing.
""".strip(),
                assigned_by="COO",
                assigned_to="Content Employee",
                priority="High",
            )
            tasks.append(task)

        if product_idea:
            dependencies = [task.id for task in tasks]
            task = self.task_manager.create_task(
                title="Create Digital Product",
                description=f"""
Create a reusable campaign asset or operating playbook based on the winning local-growth opportunity.
Opportunity: {topic}
Audience: {', '.join(audience) if audience else 'Gym owners and local adults in Hyderabad'}
Audience problem: {problem}
Product idea: {product_idea}
Recommended strategy: {strategy}
The asset must be practical, actionable, repeatable, suitable for owner review, aligned with trial-class enquiry generation, and free of unsupported health, revenue, or performance guarantees.
""".strip(),
                assigned_by="COO",
                assigned_to="Product Employee",
                priority="High",
                depends_on=dependencies,
            )
            tasks.append(task)

        return {
            "mission": topic,
            "status": "PLANNED",
            "opportunity": {
                "topic": topic,
                "problem": problem,
                "audience": audience,
                "product_idea": product_idea,
                "strategy": strategy,
            },
            "tasks": [
                {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "assigned_by": task.assigned_by,
                    "assigned_to": task.assigned_to,
                    "priority": task.priority,
                    "status": task.status,
                    "depends_on": task.depends_on,
                }
                for task in tasks
            ],
        }
