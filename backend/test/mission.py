from app.agents.mission_planner import MissionPlanner


def main():

    print("\n===== CREATOROS MISSION TEST =====\n")

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

    print(f"Mission: {mission['mission']}")
    print(f"Status: {mission['status']}")

    print("\n===== TASKS =====\n")

    for task in mission["tasks"]:

        print(f"Title: {task['title']}")
        print(f"Assigned To: {task['assigned_to']}")
        print(f"Priority: {task['priority']}")
        print(f"Status: {task['status']}")
        print(f"Description: {task['description']}")
        print("-" * 60)


if __name__ == "__main__":
    main()
