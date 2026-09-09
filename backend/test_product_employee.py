"""Manual Product Employee smoke test; use deterministic executor tests for CI."""

from app.agents.product_employee import ProductEmployee
from app.tasks.task import Task


def main():
    employee = ProductEmployee()
    task = Task(
        title="Create Digital Product",
        description="Create a reusable Hyderabad gym trial-class playbook.",
        assigned_by="COO",
        assigned_to="Product Employee",
        priority="High",
    )
    result = employee.create_product(task)
    print("\n===== PRODUCT EMPLOYEE RESULT =====\n")
    print(result)


if __name__ == "__main__":
    main()
