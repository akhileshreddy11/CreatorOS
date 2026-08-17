from app.agents.mission_planner import MissionPlanner


opportunity = {
    "topic": "AI Automation Workflows for Content Creators",
    "recommended_content": [
        "Create Instagram Reel about AI automation",
        "Create Instagram Carousel about AI tools",
        "Create YouTube Short about AI productivity"
    ],
    "product_idea": "AI Creator OS Notion Template and Prompt Pack"
}


planner = MissionPlanner()

mission = planner.create_mission(opportunity)

print("\n===== MISSION PLAN =====\n")

print("Mission:", mission["mission"])
print("Status:", mission["status"])

print("\n===== TASKS =====\n")

for task in mission["tasks"]:

    print("Title:", task["title"])
    print("Assigned To:", task["assigned_to"])
    print("Priority:", task["priority"])
    print("Status:", task["status"])
    print("Description:", task["description"])
    print("-" * 50)