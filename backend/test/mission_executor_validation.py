from app.services.mission_executor import MissionExecutor
from app.tasks.task import Task


class FakeContentEmployee:
    """
    Fake employee used to test MissionExecutor
    without calling the AI API.
    """

    def __init__(self, outputs):
        self.outputs = outputs
        self.calls = 0

    def create_content(self, task, feedback=None):

        output_index = min(
            self.calls,
            len(self.outputs) - 1
        )

        result = self.outputs[output_index]

        self.calls += 1

        return result


class FakeProductEmployee:
    """
    Fake Product Employee used to test
    MissionExecutor without calling the AI API.
    """

    def __init__(self, outputs):
        self.outputs = outputs
        self.calls = 0

    def create_product(self, task, feedback=None):

        output_index = min(
            self.calls,
            len(self.outputs) - 1
        )

        result = self.outputs[output_index]

        self.calls += 1

        return result


def valid_content():
    return {
        "hook": "Build better content workflows.",
        "script": "Use a simple workflow to organize your content.",
        "caption": "A practical content workflow.",
        "cta": "Save this for later.",
        "hashtags": [
            "#CreatorOS",
            "#ContentAutomation"
        ]
    }


def invalid_content():
    return {
        "hook": "Make $10,000 guaranteed with AI.",
        "script": "This guaranteed system will make you rich.",
        "caption": "Guaranteed results.",
        "cta": "Buy now.",
        "hashtags": [
            "#AI"
        ]
    }


def valid_product():
    return {
        "product_name": "Creator Workflow Kit",
        "tagline": "A practical creator workflow system.",
        "description": (
            "A reusable workflow system for organizing "
            "content operations."
        ),
        "target_audience": [
            "Creators",
            "Freelancers"
        ],
        "product_structure": [
            {
                "module": "Content Planning",
                "description": "Plan content efficiently.",
                "contents": [
                    "Content calendar",
                    "Approval checklist"
                ]
            }
        ],
        "prompt_pack": [
            {
                "name": "Content Planner",
                "purpose": "Plan useful content.",
                "prompt": "Create a practical content plan."
            }
        ],
        "notion_workspace": {
            "pages": [
                "Content Calendar"
            ],
            "databases": [
                "Content Database"
            ]
        },
        "automation_blueprints": [
            {
                "name": "Content Workflow",
                "purpose": "Organize content operations.",
                "workflow": [
                    "Create",
                    "Review",
                    "Approve"
                ]
            }
        ],
        "pricing": {
            "recommended_price": "Pilot pricing",
            "premium_price": "Premium pricing",
            "reason": "Based on scope and implementation effort."
        },
        "marketing_angle": (
            "A practical system for organized content operations."
        ),
        "launch_strategy": [
            "Prepare assets",
            "Review",
            "Launch pilot"
        ]
    }


def create_content_task():

    return Task(
        title="Create Instagram Reel",
        description="Create an educational AI automation reel.",
        assigned_by="COO",
        assigned_to="Content Employee",
        priority="High"
    )


def create_product_task():

    return Task(
        title="Create Creator Workflow Product",
        description="Create a reusable creator workflow product.",
        assigned_by="COO",
        assigned_to="Product Employee",
        priority="High"
    )


def test_content_success_first_attempt():

    executor = MissionExecutor()

    fake_employee = FakeContentEmployee(
        [valid_content()]
    )

    executor.content_employee = fake_employee

    task = create_content_task()

    result = executor.execute_task(task)

    assert result["status"] == "Completed"
    assert result["attempts"] == 1
    assert result["validation"]["valid"] is True
    assert fake_employee.calls == 1

    print("TEST 1: Content valid first attempt ........ PASS")


def test_content_retry_then_success():

    executor = MissionExecutor()

    fake_employee = FakeContentEmployee(
        [
            invalid_content(),
            valid_content()
        ]
    )

    executor.content_employee = fake_employee

    task = create_content_task()

    result = executor.execute_task(task)

    assert result["status"] == "Completed"
    assert result["attempts"] == 2
    assert result["validation"]["valid"] is True
    assert fake_employee.calls == 2

    print("TEST 2: Content retry then success ........ PASS")


def test_content_fails_after_three_attempts():

    executor = MissionExecutor()

    fake_employee = FakeContentEmployee(
        [
            invalid_content(),
            invalid_content(),
            invalid_content()
        ]
    )

    executor.content_employee = fake_employee

    task = create_content_task()

    result = executor.execute_task(task)

    assert result["status"] == "Failed"
    assert result["attempts"] == 3
    assert result["validation"]["valid"] is False
    assert fake_employee.calls == 3

    print("TEST 3: Content fails after 3 attempts .... PASS")


def test_product_retry_then_success():

    executor = MissionExecutor()

    fake_employee = FakeProductEmployee(
        [
            {
                "raw_content": "Malformed product output"
            },
            valid_product()
        ]
    )

    executor.product_employee = fake_employee

    task = create_product_task()

    result = executor.execute_task(task)

    assert result["status"] == "Completed"
    assert result["attempts"] == 2
    assert result["validation"]["valid"] is True
    assert fake_employee.calls == 2

    print("TEST 4: Product retry then success ........ PASS")


def test_product_fails_after_three_attempts():

    executor = MissionExecutor()

    fake_employee = FakeProductEmployee(
        [
            {
                "status": "ERROR",
                "message": "Invalid JSON",
                "raw_response": "bad"
            },
            {
                "status": "ERROR",
                "message": "Invalid JSON",
                "raw_response": "bad"
            },
            {
                "status": "ERROR",
                "message": "Invalid JSON",
                "raw_response": "bad"
            }
        ]
    )

    executor.product_employee = fake_employee

    task = create_product_task()

    result = executor.execute_task(task)

    assert result["status"] == "Failed"
    assert result["attempts"] == 3
    assert result["validation"]["valid"] is False
    assert fake_employee.calls == 3

    print("TEST 5: Product fails after 3 attempts .... PASS")


def main():

    print("\n===== MISSION EXECUTOR VALIDATION TESTS =====\n")

    test_content_success_first_attempt()
    test_content_retry_then_success()
    test_content_fails_after_three_attempts()
    test_product_retry_then_success()
    test_product_fails_after_three_attempts()

    print("\n===== ALL MISSION EXECUTOR TESTS PASSED =====\n")


if __name__ == "__main__":
    main()