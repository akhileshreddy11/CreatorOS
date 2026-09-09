from app.tasks.task import Task


class TaskManager:
    """Manage mission tasks and their dependency relationships."""

    def __init__(self):
        self.tasks = []

    def create_task(
        self,
        title,
        description,
        assigned_by,
        assigned_to,
        priority="Medium",
        depends_on=None,
    ):
        task = Task(
            title=title,
            description=description,
            assigned_by=assigned_by,
            assigned_to=assigned_to,
            priority=priority,
            depends_on=list(depends_on or []),
        )
        self.tasks.append(task)
        return task

    def start_task(self, task):
        task.start()

    def complete_task(self, task, result=None):
        task.complete(result)

    def list_tasks(self):
        return self.tasks
