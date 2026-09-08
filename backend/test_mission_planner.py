from app.agents.mission_planner import MissionPlanner


def test_mission_planner_creates_content_tasks_for_recommendations():
    planner = MissionPlanner()
    mission = planner.create_mission(
        {
            "topic": "Trial-class enquiry campaign",
            "problem": "Prospects need a clear next step.",
            "audience": ["Gym owners", "Local adults"],
            "strategy": "Use useful short videos and owner-approved follow-up.",
            "recommended_content": ["First class checklist", "Beginner questions"],
        }
    )

    assert mission["status"] == "PLANNED"
    assert len(mission["tasks"]) == 2
    assert len(planner.task_manager.tasks) == 2
    assert all(
        task["assigned_to"] == "Content Employee"
        for task in mission["tasks"]
    )
    assert all(task["status"] == "Pending" for task in mission["tasks"])


def test_mission_planner_adds_product_employee_task_when_requested():
    planner = MissionPlanner()
    mission = planner.create_mission(
        {
            "topic": "Gym pilot",
            "recommended_content": [],
            "product_idea": "A trial-class follow-up playbook",
        }
    )

    assert len(mission["tasks"]) == 1
    assert mission["tasks"][0]["assigned_to"] == "Product Employee"
    assert mission["tasks"][0]["title"] == "Create Digital Product"
    assert planner.task_manager.tasks[0].status == "Pending"


def test_mission_planner_caps_content_tasks_at_three():
    planner = MissionPlanner()
    mission = planner.create_mission(
        {"recommended_content": ["one", "two", "three", "four"]}
    )

    assert len(mission["tasks"]) == 3
    assert [task["title"] for task in mission["tasks"]] == [
        "Create Content #1",
        "Create Content #2",
        "Create Content #3",
    ]
