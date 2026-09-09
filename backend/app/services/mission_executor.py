import re
from pathlib import Path
from typing import Any, TypedDict

from app.agents.content_employee import ContentEmployee
from app.agents.product_employee import ProductEmployee
from app.services.artifact_persistence import ArtifactPersistence
from app.services.reels.reel_generator import ReelGenerator
from app.services.validation.output_validator import OutputValidator


class ExecutionResult(TypedDict, total=False):
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
    media_type: str
    media_path: str
    media_url: str


class MissionExecutor:
    """Execute a mission task graph with validation, Reel rendering and approval-gated artifacts."""

    CONTENT_EMPLOYEE = "Content Employee"
    PRODUCT_EMPLOYEE = "Product Employee"
    REEL_MARKER = "Instagram Reel-ready"

    def __init__(
        self,
        content_employee=None,
        product_employee=None,
        validator=None,
        max_attempts=3,
        artifact_persistence=None,
        reel_generator=None,
    ):
        if max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")
        self.content_employee = content_employee or ContentEmployee()
        self.product_employee = product_employee or ProductEmployee()
        self.validator = validator or OutputValidator()
        self.max_attempts = max_attempts
        self.artifact_persistence = artifact_persistence or ArtifactPersistence()
        self.reel_generator = reel_generator or ReelGenerator()

    @staticmethod
    def _safe_error(error):
        message = str(error).strip() or error.__class__.__name__
        message = re.sub(r"AIza[0-9A-Za-z_-]+", "[REDACTED_API_KEY]", message)
        message = re.sub(r"(?i)(api[_ -]?key\s*[=:]\s*)[^\s,;]+", r"\1[REDACTED]", message)
        return message[:1000]

    def _exception_validation(self, employee_name, error):
        return {
            "status": "NEEDS_REVIEW",
            "valid": False,
            "errors": [f"{employee_name} execution failed: {self._safe_error(error)}"],
            "warnings": [],
            "quality_score": 0,
        }

    @staticmethod
    def _feedback(validation):
        return [*(validation or {}).get("errors", []), *(validation or {}).get("warnings", [])]

    @staticmethod
    def _review_metadata():
        return {
            "artifact_status": "awaiting_approval",
            "approval_status": "needs_review",
            "action_class": "approval_required",
        }

    def _render_reel(self, task, result):
        """Render an explicit Reel task only after content validation succeeds."""
        if task.assigned_to != self.CONTENT_EMPLOYEE or self.REEL_MARKER not in (task.description or ""):
            return None
        output_name = f"mission_{task.id}_reel.mp4"
        path = self.reel_generator.create_reel(result, output_name=output_name, language="en")
        path_obj = Path(path)
        if not path_obj.is_file() or path_obj.stat().st_size <= 0:
            raise RuntimeError("Reel renderer did not produce a valid MP4 file.")
        return {
            "media_type": "video/mp4",
            "media_path": str(path_obj),
            "media_url": f"/media/reels/{path_obj.name}",
            "width": ReelGenerator.WIDTH,
            "height": ReelGenerator.HEIGHT,
            "fps": ReelGenerator.FPS,
        }

    def _persist_validated_artifact(self, task, employee_name, result, validation, execution):
        if employee_name == self.CONTENT_EMPLOYEE:
            execution["artifact_type"] = "content_draft"
            execution["artifact_id"] = self.artifact_persistence.persist_content(task, result, validation)
        elif employee_name == self.PRODUCT_EMPLOYEE and hasattr(self.artifact_persistence, "persist_product"):
            execution["artifact_type"] = "product_asset"
            execution["artifact_id"] = self.artifact_persistence.persist_product(task, result, validation)
        return execution

    def _failure_result(self, task, employee_name, result, validation, attempt, error=None):
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
        task.failed("; ".join(validation.get("errors", [])) if validation else "Task execution failed.", result=execution)
        return execution

    def _execute_employee_task(self, task, employee_name, employee, method_name):
        validation = None
        result = None
        last_error = None
        create_output = getattr(employee, method_name)
        for attempt in range(1, self.max_attempts + 1):
            try:
                result = create_output(task) if attempt == 1 else create_output(task, feedback=self._feedback(validation))
                validation = self.validator.validate(result, task)
                if validation["valid"]:
                    execution = {
                        "task_id": task.id,
                        "employee": employee_name,
                        "status": "Completed",
                        "result": result,
                        "validation": validation,
                        "attempts": attempt,
                    }
                    execution.update(self._review_metadata())
                    media = self._render_reel(task, result)
                    if media:
                        execution.update(media)
                        result = dict(result)
                        result["media"] = media
                        execution["result"] = result
                    execution = self._persist_validated_artifact(task, employee_name, result, validation, execution)
                    task.complete(execution)
                    return execution
                if attempt == self.max_attempts:
                    return self._failure_result(task, employee_name, result, validation, attempt)
            except Exception as error:
                last_error = error
                validation = self._exception_validation(employee_name, error)
                if attempt == self.max_attempts:
                    return self._failure_result(task, employee_name, result, validation, attempt, error)
        return self._failure_result(task, employee_name, result, validation or {"valid": False, "errors": ["Task produced no result."], "warnings": [], "quality_score": 0}, self.max_attempts, last_error)

    def execute_task(self, task, completed_ids=None):
        completed_ids = completed_ids or set()
        dependencies = getattr(task, "depends_on", []) or []
        missing = [dependency for dependency in dependencies if dependency not in completed_ids]
        if missing:
            validation = {"status": "BLOCKED", "valid": False, "errors": [f"Task dependencies are incomplete: {', '.join(missing)}"], "warnings": [], "quality_score": 0}
            return self._failure_result(task, task.assigned_to, None, validation, 0)
        if task.status in {"Completed", "Failed"}:
            return {"task_id": task.id, "employee": task.assigned_to, "status": task.status, "result": task.result, "validation": {"valid": False, "errors": [f"Task is already {task.status.lower()} and cannot be re-executed."], "warnings": [], "quality_score": 0}, "attempts": 0}
        task.start()
        if task.assigned_to == self.CONTENT_EMPLOYEE:
            return self._execute_employee_task(task, self.CONTENT_EMPLOYEE, self.content_employee, "create_content")
        if task.assigned_to == self.PRODUCT_EMPLOYEE:
            return self._execute_employee_task(task, self.PRODUCT_EMPLOYEE, self.product_employee, "create_product")
        validation = {"status": "NEEDS_REVIEW", "valid": False, "errors": [f"No employee registered for: {task.assigned_to}"], "warnings": [], "quality_score": 0}
        return self._failure_result(task, task.assigned_to, None, validation, 0)

    def execute_mission(self, tasks):
        pending = list(tasks)
        results = []
        completed_ids = set()
        while pending:
            progressed = False
            for task in list(pending):
                dependencies = getattr(task, "depends_on", []) or []
                if all(dependency in completed_ids for dependency in dependencies):
                    result = self.execute_task(task, completed_ids)
                    results.append(result)
                    pending.remove(task)
                    progressed = True
                    if result["status"] == "Completed":
                        completed_ids.add(task.id)
                    else:
                        for blocked in pending:
                            if task.id in (getattr(blocked, "depends_on", []) or []):
                                blocked.failed("A required dependency failed.")
                        return results + [{"task_id": blocked.id, "employee": blocked.assigned_to, "status": "Failed", "result": blocked.result, "validation": {"valid": False, "errors": ["Blocked by failed dependency."], "warnings": [], "quality_score": 0}, "attempts": 0} for blocked in pending]
            if not progressed:
                for task in pending:
                    task.failed("Mission contains an unresolved or circular dependency.")
                    results.append({"task_id": task.id, "employee": task.assigned_to, "status": "Failed", "result": task.result, "validation": {"valid": False, "errors": ["Unresolved or circular dependency."], "warnings": [], "quality_score": 0}, "attempts": 0})
                break
        return results
