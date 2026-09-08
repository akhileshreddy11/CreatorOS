"""Manual Mission Planner smoke test."""

from app.agents.mission_planner import MissionPlanner


def main():
    opportunity = {
        "topic": "Hyderabad gym trial-class enquiry campaign",
        "recommended_content": [
            "Create an Instagram Reel about a first gym trial class",
            "Create an Instagram Carousel about choosing a local gym",
            "Create a short video with a trial enquiry CTA",
        ],
        "product_idea": "Gym trial-class follow-up playbook",
    }

    mission = MissionPlanner().create_mission(opportunity)
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


if __name__ == "__main__":
    main()
