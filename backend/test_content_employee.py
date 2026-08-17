from app.agents.content_employee import ContentEmployee
from app.tasks.task import Task


employee = ContentEmployee()


task = Task(
    title="Create Content #1",
    description="3 AI Automation Hacks That Save Freelancers 20 Hours a Week",
    assigned_by="COO",
    assigned_to="Content Employee",
    priority="High"
)


result = employee.create_content(task)


print("\n===== CONTENT EMPLOYEE RESULT =====\n")
print(result)