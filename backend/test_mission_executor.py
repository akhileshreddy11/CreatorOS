from app.services.mission_executor import MissionExecutor
from app.tasks.task import Task


class FakeContentEmployee:
    def __init__(self, outputs):
        self.outputs = outputs
        self.calls = 0
        self.feedback = []

    def create_content(self, task, feedback=None):
        self.feedback.append(feedback)
        output = self.outputs[min(self.calls, len(self.outputs) - 1)]
        self.calls += 1
        return output


class FakeProductEmployee:
    def __init__(self, outputs):
        self.outputs = outputs
        self.calls = 0
        self.feedback = []

    def create_product(self, task, feedback=None):
        self.feedback.append(feedback)
        output = self.outputs[min(self.calls, len(self.outputs) - 1)]
        self.calls += 1
        return output


class FailingContentEmployee:
    def __init__(self):
        self.calls = 0

    def create_content(self, task, feedback=None):
        self.calls += 1
        raise RuntimeError("provider failed with api_key=secret-value")


def valid_content():
    return {
        "hook": "Build a calmer content workflow.",
        "script": "Use a simple review process to organize your content.",
        "caption": "A practical workflow for consistent publishing.",
        "cta": "Save this for your next planning session.",
        "hashtags": ["#CreatorOS", "#ContentWorkflow"],
    }


def invalid_content():
    return {
        "hook": "Make $10,000 guaranteed with AI.",
        "script": "This guaranteed system will make you rich.",
        "caption": "Guaranteed results.",
        "cta": "Buy now.",
        "hashtags": ["#AI"],
    }


def valid_product():
    return {
        "product_name": "Creator Workflow Kit",
        "tagline": "A practical creator workflow system.",
        "description": "A reusable system for organizing content operations.",
        "target_audience": ["Creators", "Freelancers"],
        "product_structure": [
            {
                "module": "Content Planning",
                "description": "Plan content efficiently.",
                "contents": ["Content calendar", "Approval checklist"],
            }
        ],
        "prompt_pack": [
            {
                "name": "Content Planner",
                "purpose": "Plan useful content.",
                "prompt": "Create a practical content plan.",
            }
        ],
        "notion_workspace": {
            "pages": ["Content Calendar"],
            "databases": ["Content Database"],
        },
        "automation_blueprints": [
            {
                "name": "Content Workflow",
                "purpose": "Organize content operations.",
                "workflow": ["Create", "Review", "Approve"],
            }
        ],
        "pricing": {
            "recommended_price": "Pilot pricing",
            "premium_price": "Premium pricing",
            "reason": "Based on scope and implementation effort.",
        },
        "marketing_angle": "A practical system for organized operations.",
        "launch_strategy": ["Prepare assets", "Review", "Launch pilot"],
    }


def content_task():
    return Task(
        title="Create Instagram Reel",
        description="Create an educational gym content piece.",
        assigned_by="COO",
        assigned_to="Content Employee",
        priority="High",
    )


def product_task():
    return Task(
        title="Create Creator Workflow Product",
        description="Create a reusable creator workflow product.",
        assigned_by="COO",
        assigned_to="Product Employee",
        priority="High",
    )


def test_content_success_starts_and_completes_task():
    employee = FakeContentEmployee([valid_content()])
    task = content_task()
    result = MissionExecutor(
        content_employee=employee,
        product_employee=FakeProductEmployee([valid_product()]),
    ).execute_task(task)

    assert result["status"] == "Completed"
    assert result["attempts"] == 1
    assert result["validation"]["valid"] is True
    assert result["approval_status"] == "needs_review"
    assert result["action_class"] == "approval_required"
    assert result["artifact_status"] == "awaiting_approval"
    assert task.status == "Completed"
    assert employee.calls == 1


def test_content_retry_passes_validator_feedback_then_succeeds():
    employee = FakeContentEmployee([invalid_content(), valid_content()])
    task = content_task()
    result = MissionExecutor(
        content_employee=employee,
        product_employee=FakeProductEmployee([valid_product()]),
    ).execute_task(task)

    assert result["status"] == "Completed"
    assert result["attempts"] == 2
    assert employee.calls == 2
    assert employee.feedback[0] is None
    assert employee.feedback[1]
    assert any("claim" in item.lower() for item in employee.feedback[1])


def test_content_fails_after_retry_limit():
    employee = FakeContentEmployee([invalid_content()])
    task = content_task()
    result = MissionExecutor(
        content_employee=employee,
        product_employee=FakeProductEmployee([valid_product()]),
    ).execute_task(task)

    assert result["status"] == "Failed"
    assert result["attempts"] == 3
    assert result["validation"]["valid"] is False
    assert task.status == "Failed"
    assert employee.calls == 3


def test_product_retry_then_success_is_reviewable():
    employee = FakeProductEmployee(
        [{"raw_content": "Malformed product output"}, valid_product()]
    )
    task = product_task()
    result = MissionExecutor(
        content_employee=FakeContentEmployee([valid_content()]),
        product_employee=employee,
    ).execute_task(task)

    assert result["status"] == "Completed"
    assert result["attempts"] == 2
    assert result["validation"]["valid"] is True
    assert result["approval_status"] == "needs_review"
    assert result["artifact_status"] == "awaiting_approval"
    assert task.status == "Completed"


def test_product_fails_after_retry_limit():
    employee = FakeProductEmployee([{"status": "ERROR", "raw_response": "bad"}])
    task = product_task()
    result = MissionExecutor(
        content_employee=FakeContentEmployee([valid_content()]),
        product_employee=employee,
    ).execute_task(task)

    assert result["status"] == "Failed"
    assert result["attempts"] == 3
    assert result["validation"]["valid"] is False
    assert task.status == "Failed"
    assert employee.calls == 3


def test_provider_failure_is_safe_and_structured():
    employee = FailingContentEmployee()
    task = content_task()
    result = MissionExecutor(
        content_employee=employee,
        product_employee=FakeProductEmployee([valid_product()]),
    ).execute_task(task)

    assert result["status"] == "Failed"
    assert result["attempts"] == 3
    assert result["validation"]["valid"] is False
    assert "secret-value" not in result["error"]
    assert "api_key=[REDACTED]" in result["error"]
    assert task.status == "Failed"
