import json

from app.agents.mission_planner import MissionPlanner
from app.services.mission_executor import MissionExecutor


def main():

    print("\n===== CREATOROS MISSION EXECUTION =====\n")

    # -----------------------------------------
    # STEP 1: Create the mission
    # -----------------------------------------

    planner = MissionPlanner()

    opportunity = {
        "topic": "AI Automation Workflows for Content Creators",

        "recommended_content": [
            "Create Instagram Reel about AI automation",
            "Create Instagram Carousel about AI tools",
            "Create YouTube Short about AI productivity"
        ],

        "product_idea": "AI Creator OS Notion Template and Prompt Pack"
    }

    mission = planner.create_mission(opportunity)

    print("Mission:", mission["mission"])
    print("Status:", mission["status"])

    print("\n===== PLANNED TASKS =====\n")

    for task in mission["tasks"]:
        print("Title:", task["title"])
        print("Assigned To:", task["assigned_to"])
        print("Priority:", task["priority"])
        print("Status:", task["status"])
        print("---")

    # -----------------------------------------
    # STEP 2: Re-create task objects
    # -----------------------------------------

    tasks = planner.task_manager.tasks

    print("\n===== EXECUTING MISSION =====\n")

    # -----------------------------------------
    # STEP 3: Execute all tasks
    # -----------------------------------------

    executor = MissionExecutor()

    results = executor.execute_mission(tasks)

    # -----------------------------------------
    # STEP 4: Display results
    # -----------------------------------------

    for result in results:

        print("\n========================================")
        print("Task ID:", result["task_id"])
        print("Employee:", result["employee"])
        print("Status:", result["status"])

        print("\nResult:")

        if isinstance(result["result"], (dict, list)):
            print(
                json.dumps(
                    result["result"],
                    indent=2,
                    ensure_ascii=False
                )
            )
        else:
            print(result["result"])

    print("\n========================================")
    print("\n===== MISSION EXECUTION COMPLETE =====\n")


if __name__ == "__main__":
    main()