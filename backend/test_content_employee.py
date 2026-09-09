"""Manual Content Employee smoke test; use test_mission_executor.py for CI."""

from app.agents.content_employee import ContentEmployee
from app.tasks.task import Task


def main():
    employee = ContentEmployee()
    task = Task(
        title="Create Content #1",
        description="Create a claim-safe Hyderabad gym content piece.",
        assigned_by="COO",
        assigned_to="Content Employee",
        priority="High",
    )
    result = employee.create_content(task)
    print("\n===== CONTENT EMPLOYEE RESULT =====\n")
    print(result)


if __name__ == "__main__":
    main()
