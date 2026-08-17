from app.agents.product_employee import ProductEmployee
from app.tasks.task import Task


# Create Product Employee
employee = ProductEmployee()


# Create a test task
task = Task(
    title="Create Digital Product",
    description=(
        "The Autonomous Creator OS Toolkit: "
        "AI Prompts, Notion Workspaces, and Automation Blueprints"
    ),
    assigned_by="COO",
    assigned_to="Product Employee",
    priority="High"
)


# Execute the task
result = employee.create_product(task)


print("\n===== PRODUCT EMPLOYEE RESULT =====\n")

print(result)