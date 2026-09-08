import re
from typing import Any, TypedDict

from app.agents.content_employee import ContentEmployee
from app.agents.product_employee import ProductEmployee
from app.services.artifact_persistence import ArtifactPersistence
from app.services.validation.output_validator import OutputValidator


class ExecutionResult(TypedDict, total=False):
    """Runtime shape returned for every attempted task execution."""

    task_id: str
    employee: str
    status: str
    result: Any
    validation: dict
    attempts: int
    artifact_status: str
    approval_status: str
    action_class: str
    artifact_type: str
    artifact_id: int
    error: str


class MissionExecutor:
    """
    CreatorOS Mission Execution Engine

    Executes tasks through AI employees and validates their outputs before
    marking tasks as completed.

    Validated content artifacts are persisted into the CreatorOS approval
    system so they can appear in the Drafts interface.

    Publishing, sending, and optional media rendering remain outside
    this executor and require owner approval.
    """

    CONTENT_EMPLOYEE = "Content Employee"
    PRODUCT_EMPLOYEE = "Product Employee"

    def __init__(
        self,
        content_employee=None,
        product_employee=None,
        validator=None,
        max_attempts=3,
        artifact_persistence=None,
    ):
        if max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")

        self.content_employee = (
            content_employee
            if content_employee is not None
            else ContentEmployee()
        )

        self.product_employee = (
            product_employee
            if product_employee is not None
            else ProductEmployee()
        )

        self.validator = validator or OutputValidator()

        self.max_attempts = max_attempts

        self.artifact_persistence = (
            artifact_persistence
            if artifact_persistence is not None
            else ArtifactPersistence()
        )

    # -----------------------------------------
    # SHARED EXECUTION HELPERS
    # -----------------------------------------

    @staticmethod
    def _safe_error(error):
        """
        Return useful provider diagnostics without exposing credentials.
        """

        message = str(error).strip() or error.__class__.__name__

        message = re.sub(
            r"AIza[0-9A-Za-z_-]+",
            "[REDACTED_API_KEY]",
            message,
        )

        message = re.sub(
            r"(?i)(api[_ -]?key\s*[=:]\s*)[^\s,;]+",
            r"\1[REDACTED]",
            message,
        )

        return message[:1000]

    def _exception_validation(self, employee_name, error):
        """
        Convert an employee exception into the same validation shape
        used by OutputValidator.
        """

        message = self._safe_error(error)

        return {
            "status": "NEEDS_REVIEW",
            "valid": False,
            "errors": [
                f"{employee_name} execution failed: {message}"
            ],
            "warnings": [],
            "quality_score": 0,
        }

    @staticmethod
    def _feedback(validation):
        """
        Convert validator feedback into feedback that can be sent
        back to an AI employee during retry.
        """

        if not validation:
            return []

        return [
            *validation.get("errors", []),
            *validation.get("warnings", []),
        ]

    @staticmethod
    def _review_metadata():
        """
        Metadata attached to successfully validated artifacts.

        Validation approval does NOT mean owner approval.
        """

        return {
            "artifact_status": "awaiting_approval",
            "approval_status": "needs_review",
            "action_class": "approval_required",
        }

    def _success_result(
        self,
        task,
        employee_name,
        result,
        validation,
        attempt,
    ):
        """
        Build the standard successful execution response.
        """

        execution = {
            "task_id": task.id,
            "employee": employee_name,
            "status": "Completed",
            "result": result,
            "validation": validation,
            "attempts": attempt,
        }

        execution.update(
            self._review_metadata()
        )

        return execution

    def _failure_result(
        self,
        task,
        employee_name,
        result,
        validation,
        attempt,
        error=None,
    ):
        """
        Build the standard failed execution response.
        """

        execution = {
            "task_id": task.id,
            "employee": employee_name,
            "status": "Failed",
            "result": result,
            "validation": validation,
            "attempts": attempt,
        }

        if error:
            execution["error"] = self._safe_error(error)

        task.failed(
            "; ".join(
                validation.get("errors", [])
            )
            if validation
            else "Task execution failed.",
            result=execution,
        )

        return execution

    # -----------------------------------------
    # ARTIFACT PERSISTENCE
    # -----------------------------------------

    def _persist_validated_artifact(
        self,
        task,
        employee_name,
        result,
        validation,
        execution,
    ):
        """
        Persist validated AI output into the appropriate CreatorOS
        artifact system.

        Content Employee output is currently persisted into ContentDraft.

        Product Employee persistence is intentionally left unchanged until
        CreatorOS has a dedicated product artifact model.
        """

        if employee_name == self.CONTENT_EMPLOYEE:

            draft_id = self.artifact_persistence.persist_content(
                task=task,
                result=result,
                validation=validation,
            )

            execution["artifact_type"] = "content_draft"
            execution["artifact_id"] = draft_id

        elif employee_name == self.PRODUCT_EMPLOYEE:

            if hasattr(self.artifact_persistence, "persist_product"):
                try:
                    draft_id = self.artifact_persistence.persist_product(
                        task=task,
                        result=result,
                        validation=validation,
                    )
                    execution["artifact_type"] = "product_asset"
                    execution["artifact_id"] = draft_id
                except Exception as e:
                    print(f"[MissionExecutor] Product persistence note: {e}")

        return execution

    # -----------------------------------------
    # EXECUTE EMPLOYEE TASK
    # -----------------------------------------

    def _execute_employee_task(
        self,
        task,
        employee_name,
        employee,
        method_name,
    ):
        validation = None
        result = None
        last_error = None

        create_output = getattr(
            employee,
            method_name,
        )

        for attempt in range(
            1,
            self.max_attempts + 1,
        ):

            try:

                # -----------------------------------------
                # GENERATE OUTPUT
                # -----------------------------------------

                if attempt == 1:

                    result = create_output(task)

                else:

                    result = create_output(
                        task,
                        feedback=self._feedback(
                            validation
                        ),
                    )

                # -----------------------------------------
                # VALIDATE OUTPUT
                # -----------------------------------------

                validation = self.validator.validate(
                    result,
                    task,
                )

                print(
                    f"\n[{employee_name}] "
                    f"Validation attempt "
                    f"{attempt}/{self.max_attempts}: "
                    f"{validation['status']}"
                )

                # -----------------------------------------
                # VALID OUTPUT
                # -----------------------------------------

                if validation["valid"]:

                    execution = self._success_result(
                        task,
                        employee_name,
                        result,
                        validation,
                        attempt,
                    )

                    # -----------------------------------------
                    # PERSIST VALIDATED ARTIFACT
                    # -----------------------------------------

                    execution = self._persist_validated_artifact(
                        task=task,
                        employee_name=employee_name,
                        result=result,
                        validation=validation,
                        execution=execution,
                    )

                    # -----------------------------------------
                    # COMPLETE TASK
                    # -----------------------------------------

                    task.complete(
                        execution
                    )

                    return execution

                # -----------------------------------------
                # INVALID OUTPUT
                # -----------------------------------------

                last_error = None

                if attempt < self.max_attempts:

                    print(
                        f"[{employee_name}] "
                        "Output rejected. Sending "
                        "validation feedback back "
                        "to employee..."
                    )

                    continue

                # -----------------------------------------
                # ALL VALIDATION ATTEMPTS FAILED
                # -----------------------------------------

                return self._failure_result(
                    task=task,
                    employee_name=employee_name,
                    result=result,
                    validation=validation,
                    attempt=attempt,
                )

            except Exception as error:

                last_error = error

                validation = self._exception_validation(
                    employee_name,
                    error,
                )

                print(
                    f"\n[{employee_name}] "
                    f"Execution attempt "
                    f"{attempt}/{self.max_attempts} failed: "
                    f"{validation['errors'][0]}"
                )

                # -----------------------------------------
                # RETRY EXCEPTION
                # -----------------------------------------

                if attempt < self.max_attempts:

                    continue

                # -----------------------------------------
                # ALL EXECUTION ATTEMPTS FAILED
                # -----------------------------------------

                return self._failure_result(
                    task=task,
                    employee_name=employee_name,
                    result=result,
                    validation=validation,
                    attempt=attempt,
                    error=last_error,
                )

        # -----------------------------------------
        # DEFENSIVE FALLBACK
        # -----------------------------------------

        validation = validation or {
            "status": "NEEDS_REVIEW",
            "valid": False,
            "errors": [
                "Task execution did not produce a result."
            ],
            "warnings": [],
            "quality_score": 0,
        }

        return self._failure_result(
            task=task,
            employee_name=employee_name,
            result=result,
            validation=validation,
            attempt=self.max_attempts,
            error=last_error,
        )

    # -----------------------------------------
    # EXECUTE SINGLE TASK
    # -----------------------------------------

    def execute_task(self, task):

        # -----------------------------------------
        # PREVENT DUPLICATE EXECUTION
        # -----------------------------------------

        if task.status in {
            "Completed",
            "Failed",
        }:

            validation = {
                "status": "NEEDS_REVIEW",
                "valid": False,
                "errors": [
                    (
                        f"Task is already "
                        f"{task.status.lower()} "
                        "and cannot be re-executed."
                    )
                ],
                "warnings": [],
                "quality_score": 0,
            }

            return {
                "task_id": task.id,
                "employee": task.assigned_to,
                "status": task.status,
                "result": task.result,
                "validation": validation,
                "attempts": 0,
                "error": validation["errors"][0],
            }

        # -----------------------------------------
        # START TASK
        # -----------------------------------------

        task.start()

        # -----------------------------------------
        # CONTENT EMPLOYEE
        # -----------------------------------------

        if task.assigned_to == self.CONTENT_EMPLOYEE:

            return self._execute_employee_task(
                task,
                self.CONTENT_EMPLOYEE,
                self.content_employee,
                "create_content",
            )

        # -----------------------------------------
        # PRODUCT EMPLOYEE
        # -----------------------------------------

        if task.assigned_to == self.PRODUCT_EMPLOYEE:

            return self._execute_employee_task(
                task,
                self.PRODUCT_EMPLOYEE,
                self.product_employee,
                "create_product",
            )

        # -----------------------------------------
        # UNKNOWN EMPLOYEE
        # -----------------------------------------

        validation = {
            "status": "NEEDS_REVIEW",
            "valid": False,
            "errors": [
                (
                    "No employee registered for: "
                    f"{task.assigned_to}"
                )
            ],
            "warnings": [],
            "quality_score": 0,
        }

        return self._failure_result(
            task=task,
            employee_name=task.assigned_to,
            result=None,
            validation=validation,
            attempt=0,
        )

    # -----------------------------------------
    # EXECUTE COMPLETE MISSION
    # -----------------------------------------

    def execute_mission(self, tasks):

        return [
            self.execute_task(task)
            for task in tasks
        ]