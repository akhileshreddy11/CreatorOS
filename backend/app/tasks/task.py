from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4
from typing import Optional


@dataclass
class Task:
    """A business task exchanged between CreatorOS AI employees."""

    id: str = field(default_factory=lambda: str(uuid4()))
    title: str = ""
    description: str = ""
    assigned_by: str = ""
    assigned_to: str = ""
    priority: str = "Medium"
    status: str = "Pending"
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    result: Optional[dict] = None
    depends_on: list[str] = field(default_factory=list)

    def start(self):
        if self.status in {"Completed", "Failed"}:
            raise RuntimeError(f"Task is already {self.status.lower()}.")
        self.status = "In Progress"

    def complete(self, result=None):
        self.status = "Completed"
        self.completed_at = datetime.now()
        self.result = result

    def failed(self, reason, result=None):
        self.status = "Failed"
        self.completed_at = datetime.now()
        self.result = result if result is not None else {"reason": reason}
