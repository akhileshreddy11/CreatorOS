from app.agents.content_employee import ContentEmployee
from app.agents.product_employee import ProductEmployee
from app.services.validation.output_validator import OutputValidator


class MissionExecutor:
    """
    CreatorOS Mission Execution Engine

    Executes tasks through AI employees and validates
    their outputs before marking tasks as completed.

    Validated content is returned as a reviewable artifact.  Publishing
    or optional media rendering must happen only after owner approval.
    """

    def __init__(self):
        self.content_employee = ContentEmployee()
        self.product_employee = ProductEmployee()
        self.validator = OutputValidator()
        self.max_attempts = 3

    # -----------------------------------------
    # CONTENT EMPLOYEE
    # -----------------------------------------

    def _execute_content_task(self, task):

        validation = None
        result = None

        for attempt in range(1, self.max_attempts + 1):

            try:

                if attempt == 1:

                    result = self.content_employee.create_content(task)

                else:

                    feedback = []

                    if validation:
                        feedback.extend(
                            validation.get("errors", [])
                        )

                        feedback.extend(
                            validation.get("warnings", [])
                        )

                    result = self.content_employee.create_content(
                        task,
                        feedback=feedback
                    )

                # -----------------------------------------
                # VALIDATE CONTENT
                # -----------------------------------------

                validation = self.validator.validate(
                    result,
                    task
                )

                print(
                    f"\n[Content Employee] "
                    f"Validation attempt {attempt}/{self.max_attempts}: "
                    f"{validation['status']}"
                )

                # -----------------------------------------
                # VALID OUTPUT
                # -----------------------------------------

                if validation["valid"]:

                    # Keep the validated output in the approval queue.  A
                    # media artifact can be rendered after owner approval.
                    result["approval_status"] = "needs_review"
                    result["action_class"] = "approval_required"
                    task.complete(result)

                    return {
                        "task_id": task.id,
                        "employee": "Content Employee",
                        "status": task.status,
                        "result": result,
                        "validation": validation,
                        "artifact_status": "awaiting_approval",
                        "attempts": attempt
                    }

                # -----------------------------------------
                # INVALID OUTPUT
                # -----------------------------------------

                if attempt < self.max_attempts:

                    print(
                        "[Content Employee] "
                        "Output rejected. Sending validation "
                        "feedback back to employee..."
                    )

                    continue

                # -----------------------------------------
                # ALL ATTEMPTS FAILED
                # -----------------------------------------

                task.failed(
                    "Output validation failed after "
                    f"{self.max_attempts} attempts: "
                    + "; ".join(
                        validation["errors"]
                    )
                )

                return {
                    "task_id": task.id,
                    "employee": "Content Employee",
                    "status": task.status,
                    "result": result,
                    "validation": validation,
                    "attempts": attempt
                }

            except Exception as error:

                task.failed(str(error))

                return {
                    "task_id": task.id,
                    "employee": "Content Employee",
                    "status": task.status,
                    "result": task.result
                }

    # -----------------------------------------
    # PRODUCT EMPLOYEE
    # -----------------------------------------

    def _execute_product_task(self, task):

        validation = None
        result = None

        for attempt in range(1, self.max_attempts + 1):

            try:

                if attempt == 1:

                    result = self.product_employee.create_product(task)

                else:

                    feedback = []

                    if validation:
                        feedback.extend(
                            validation.get("errors", [])
                        )

                        feedback.extend(
                            validation.get("warnings", [])
                        )

                    result = self.product_employee.create_product(
                        task,
                        feedback=feedback
                    )

                # -----------------------------------------
                # VALIDATE PRODUCT
                # -----------------------------------------

                validation = self.validator.validate(
                    result,
                    task
                )

                print(
                    f"\n[Product Employee] "
                    f"Validation attempt {attempt}/{self.max_attempts}: "
                    f"{validation['status']}"
                )

                # -----------------------------------------
                # VALID OUTPUT
                # -----------------------------------------

                if validation["valid"]:

                    task.complete(result)

                    return {
                        "task_id": task.id,
                        "employee": "Product Employee",
                        "status": task.status,
                        "result": result,
                        "validation": validation,
                        "attempts": attempt
                    }

                # -----------------------------------------
                # INVALID OUTPUT
                # -----------------------------------------

                if attempt < self.max_attempts:

                    print(
                        "[Product Employee] "
                        "Output rejected. Sending validation "
                        "feedback back to employee..."
                    )

                    continue

                # -----------------------------------------
                # ALL ATTEMPTS FAILED
                # -----------------------------------------

                task.failed(
                    "Output validation failed after "
                    f"{self.max_attempts} attempts: "
                    + "; ".join(
                        validation["errors"]
                    )
                )

                return {
                    "task_id": task.id,
                    "employee": "Product Employee",
                    "status": task.status,
                    "result": result,
                    "validation": validation,
                    "attempts": attempt
                }

            except Exception as error:

                task.failed(str(error))

                return {
                    "task_id": task.id,
                    "employee": "Product Employee",
                    "status": task.status,
                    "result": task.result
                }

    # -----------------------------------------
    # EXECUTE SINGLE TASK
    # -----------------------------------------

    def execute_task(self, task):

        if task.assigned_to == "Content Employee":

            return self._execute_content_task(task)

        elif task.assigned_to == "Product Employee":

            return self._execute_product_task(task)

        else:

            task.failed(
                f"No employee registered for: "
                f"{task.assigned_to}"
            )

            return {
                "task_id": task.id,
                "employee": task.assigned_to,
                "status": task.status,
                "result": task.result
            }

    # -----------------------------------------
    # EXECUTE COMPLETE MISSION
    # -----------------------------------------

    def execute_mission(self, tasks):

        results = []

        for task in tasks:

            result = self.execute_task(task)

            results.append(result)

        return results