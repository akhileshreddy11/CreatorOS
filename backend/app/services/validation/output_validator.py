import re


class OutputValidator:
    """
    CreatorOS Output Validator

    Strictly validates AI employee output before it is
    accepted by the Mission Execution Engine.

    Validation covers:
    - Output shape
    - Required fields
    - Field types
    - Unknown/error-shaped responses
    - Unsupported guarantees
    - Unsupported income claims
    - Unsupported performance claims
    - Numeric performance claims
    - Basic content quality
    - Product output quality
    """

    CONTENT_EMPLOYEE = "Content Employee"
    PRODUCT_EMPLOYEE = "Product Employee"

    def __init__(self):

        self.forbidden_patterns = [

            # Guarantees
            r"\bguaranteed\b",
            r"\bguarantee(?:d|s)?\b",
            r"\bguaranteed income\b",
            r"\bguaranteed results\b",
            r"\bguaranteed profit\b",

            # Income claims
            r"\bmake \$\d+",
            r"\bearn \$\d+",
            r"\bmake \d+% more\b",
            r"\bearn \d+% more\b",

            # Personal experience claims
            r"\bi used to\b",
            r"\bi saved\b",
            r"\bi save\b",
            r"\bi earned\b",
            r"\bi made \$\d+",
            r"\bi generated \$\d+",
            r"\bi gained\b",
            r"\bi grew\b",
            r"\bmy results\b",
            r"\bmy revenue\b",

            # First-person performance claims
            r"\bsaves me\b",
            r"\bsaved me\b",
            r"\bmade me\b",
            r"\bearned me\b",
            r"\bhelped me make\b",

            # Strong unsupported performance language
            r"\bslashes\b.*\btime\b",
            r"\b\d+%\b.*\b(faster|more|less|increase|decrease|growth)\b",
            r"\b(faster|more|less)\b.*\b\d+%\b",

            # Unsupported viral/performance claims
            r"\bviral-ready\b",
            r"\bviral content\b",
            r"\bhigh-performing\b",
            r"\bhigh converting\b",
            r"\bhigh-converting\b",
        ]

        self.statistic_patterns = [
            r"\b\d+%\b",
            r"\b\d+\+\s*(hours|followers|views|customers|clients)\b",
            r"\b\d+\s*(hours|followers|views|customers|clients)\b",
            r"\b\d+-\d+\s*(hours|followers|views|customers|clients)\b",
        ]

    # -----------------------------------------
    # PUBLIC VALIDATION METHOD
    # -----------------------------------------

    def validate(self, result, task=None):

        errors = []
        warnings = []

        # -----------------------------------------
        # BASIC TYPE CHECK
        # -----------------------------------------

        if result is None:
            return self._failure(
                ["AI returned no output."]
            )

        if not isinstance(result, dict):
            return self._failure(
                ["AI output must be a JSON object."]
            )

        # -----------------------------------------
        # REJECT ERROR-SHAPED OUTPUT
        # -----------------------------------------

        if self._is_error_output(result):
            return self._failure(
                ["AI employee returned an error-shaped or malformed output."]
            )

        # -----------------------------------------
        # DETERMINE EXPECTED EMPLOYEE
        # -----------------------------------------

        employee = None

        if task is not None:
            employee = getattr(task, "assigned_to", None)

        # -----------------------------------------
        # STRICT STRUCTURE VALIDATION
        # -----------------------------------------

        if employee == self.CONTENT_EMPLOYEE:

            errors.extend(
                self._validate_content_structure(result)
            )

        elif employee == self.PRODUCT_EMPLOYEE:

            errors.extend(
                self._validate_product_structure(result)
            )

        else:

            # Preserve compatibility with the existing
            # validator test that calls validate(result)
            # without a Task.
            detected_type = self._detect_output_type(result)

            if detected_type == "content":
                errors.extend(
                    self._validate_content_structure(result)
                )

            elif detected_type == "product":
                errors.extend(
                    self._validate_product_structure(result)
                )

            else:
                errors.append(
                    "AI output does not match a recognized "
                    "Content Employee or Product Employee schema."
                )

        # -----------------------------------------
        # CONVERT OUTPUT TO SEARCHABLE TEXT
        # -----------------------------------------

        text = self._flatten_to_text(result)

        # -----------------------------------------
        # CHECK FOR FORBIDDEN CLAIMS
        # -----------------------------------------

        for pattern in self.forbidden_patterns:

            if re.search(
                pattern,
                text,
                re.IGNORECASE
            ):

                errors.append(
                    "Potential unsupported guarantee, "
                    "personal experience, or performance "
                    "claim detected."
                )

                break

        # -----------------------------------------
        # CHECK STATISTICS
        # -----------------------------------------

        for pattern in self.statistic_patterns:

            if re.search(
                pattern,
                text,
                re.IGNORECASE
            ):

                warnings.append(
                    "Numeric performance claim detected. "
                    "Verify that the claim is supported "
                    "before publishing."
                )

                break

        # -----------------------------------------
        # EMPTY OUTPUT CHECK
        # -----------------------------------------

        if not text.strip():

            errors.append(
                "AI returned an empty result."
            )

        # -----------------------------------------
        # FINAL DECISION
        # -----------------------------------------

        if errors:

            return self._failure(
                errors=errors,
                warnings=warnings
            )

        return {
            "status": "APPROVED",
            "valid": True,
            "errors": [],
            "warnings": warnings,
            "quality_score": self._calculate_score(
                result,
                warnings
            )
        }

    # -----------------------------------------
    # CONTENT STRUCTURE
    # -----------------------------------------

    def _validate_content_structure(self, result):

        errors = []

        required_fields = {
            "hook",
            "script",
            "caption",
            "cta",
            "hashtags",
        }

        errors.extend(
            self._validate_exact_keys(
                result,
                required_fields,
                "content"
            )
        )

        string_fields = [
            "hook",
            "script",
            "caption",
            "cta",
        ]

        for field in string_fields:

            if field in result and not isinstance(
                result[field],
                str
            ):

                errors.append(
                    f"Content field '{field}' must be a string."
                )

            elif field in result and not result[field].strip():

                errors.append(
                    f"Content field '{field}' cannot be empty."
                )

        if "hashtags" in result:

            hashtags = result["hashtags"]

            if not isinstance(hashtags, list):

                errors.append(
                    "Content field 'hashtags' must be a list."
                )

            else:

                if not hashtags:

                    errors.append(
                        "Content field 'hashtags' cannot be empty."
                    )

                for index, hashtag in enumerate(hashtags):

                    if not isinstance(hashtag, str):

                        errors.append(
                            f"Hashtag at index {index} must be a string."
                        )

                    elif not hashtag.strip():

                        errors.append(
                            f"Hashtag at index {index} cannot be empty."
                        )

        return errors

    # -----------------------------------------
    # PRODUCT STRUCTURE
    # -----------------------------------------

    def _validate_product_structure(self, result):

        errors = []

        required_fields = {
            "product_name",
            "tagline",
            "description",
            "target_audience",
            "product_structure",
            "prompt_pack",
            "notion_workspace",
            "automation_blueprints",
            "pricing",
            "marketing_angle",
            "launch_strategy",
        }

        errors.extend(
            self._validate_exact_keys(
                result,
                required_fields,
                "product"
            )
        )

        # String fields

        string_fields = [
            "product_name",
            "tagline",
            "description",
            "marketing_angle",
        ]

        for field in string_fields:

            if field in result and not isinstance(
                result[field],
                str
            ):

                errors.append(
                    f"Product field '{field}' must be a string."
                )

            elif field in result and not result[field].strip():

                errors.append(
                    f"Product field '{field}' cannot be empty."
                )

        # List fields

        list_fields = [
            "target_audience",
            "product_structure",
            "prompt_pack",
            "automation_blueprints",
            "launch_strategy",
        ]

        for field in list_fields:

            if field in result and not isinstance(
                result[field],
                list
            ):

                errors.append(
                    f"Product field '{field}' must be a list."
                )

        # Target audience

        if isinstance(
            result.get("target_audience"),
            list
        ):

            for index, item in enumerate(
                result["target_audience"]
            ):

                if not isinstance(item, str):

                    errors.append(
                        "target_audience items must be strings."
                    )

        # Product structure

        if isinstance(
            result.get("product_structure"),
            list
        ):

            for index, item in enumerate(
                result["product_structure"]
            ):

                if not isinstance(item, dict):

                    errors.append(
                        f"product_structure item {index} must be an object."
                    )
                    continue

                for field in [
                    "module",
                    "description",
                    "contents",
                ]:

                    if field not in item:

                        errors.append(
                            f"product_structure item {index} "
                            f"is missing '{field}'."
                        )

                if "module" in item and not isinstance(
                    item["module"],
                    str
                ):

                    errors.append(
                        f"product_structure item {index} "
                        "'module' must be a string."
                    )

                if "description" in item and not isinstance(
                    item["description"],
                    str
                ):

                    errors.append(
                        f"product_structure item {index} "
                        "'description' must be a string."
                    )

                if "contents" in item and not isinstance(
                    item["contents"],
                    list
                ):

                    errors.append(
                        f"product_structure item {index} "
                        "'contents' must be a list."
                    )

                elif isinstance(
                    item.get("contents"),
                    list
                ):

                    for content in item["contents"]:

                        if not isinstance(
                            content,
                            str
                        ):

                            errors.append(
                                "product_structure contents "
                                "must contain only strings."
                            )

        # Prompt pack

        if isinstance(
            result.get("prompt_pack"),
            list
        ):

            for index, item in enumerate(
                result["prompt_pack"]
            ):

                if not isinstance(item, dict):

                    errors.append(
                        f"prompt_pack item {index} must be an object."
                    )
                    continue

                for field in [
                    "name",
                    "purpose",
                    "prompt",
                ]:

                    if field not in item:

                        errors.append(
                            f"prompt_pack item {index} "
                            f"is missing '{field}'."
                        )

                    elif not isinstance(
                        item[field],
                        str
                    ):

                        errors.append(
                            f"prompt_pack item {index} "
                            f"'{field}' must be a string."
                        )

        # Notion workspace

        notion = result.get("notion_workspace")

        if notion is not None:

            if not isinstance(notion, dict):

                errors.append(
                    "notion_workspace must be an object."
                )

            else:

                for field in [
                    "pages",
                    "databases",
                ]:

                    if field not in notion:

                        errors.append(
                            f"notion_workspace is missing '{field}'."
                        )

                    elif not isinstance(
                        notion[field],
                        list
                    ):

                        errors.append(
                            f"notion_workspace '{field}' "
                            "must be a list."
                        )

        # Automation blueprints

        if isinstance(
            result.get("automation_blueprints"),
            list
        ):

            for index, item in enumerate(
                result["automation_blueprints"]
            ):

                if not isinstance(item, dict):

                    errors.append(
                        f"automation_blueprints item {index} "
                        "must be an object."
                    )
                    continue

                for field in [
                    "name",
                    "purpose",
                    "workflow",
                ]:

                    if field not in item:

                        errors.append(
                            f"automation_blueprints item {index} "
                            f"is missing '{field}'."
                        )

                    elif field in item and field != "workflow" and not isinstance(
                        item[field],
                        str
                    ):

                        errors.append(
                            f"automation_blueprints item {index} "
                            f"'{field}' must be a string."
                        )

                if "workflow" in item and not isinstance(
                    item["workflow"],
                    list
                ):

                    errors.append(
                        f"automation_blueprints item {index} "
                        "'workflow' must be a list."
                    )

        # Pricing

        pricing = result.get("pricing")

        if pricing is not None:

            if not isinstance(pricing, dict):

                errors.append(
                    "pricing must be an object."
                )

            else:

                for field in [
                    "recommended_price",
                    "premium_price",
                    "reason",
                ]:

                    if field not in pricing:

                        errors.append(
                            f"pricing is missing '{field}'."
                        )

                    elif not isinstance(
                        pricing[field],
                        str
                    ):

                        errors.append(
                            f"pricing '{field}' must be a string."
                        )

        return errors

    # -----------------------------------------
    # EXACT KEY VALIDATION
    # -----------------------------------------

    def _validate_exact_keys(
        self,
        result,
        required_fields,
        output_name
    ):

        errors = []

        actual_keys = set(result.keys())

        missing = required_fields - actual_keys

        unknown = actual_keys - required_fields

        if missing:

            errors.append(
                f"Missing required {output_name} fields: "
                + ", ".join(sorted(missing))
            )

        if unknown:

            errors.append(
                f"Unknown {output_name} fields: "
                + ", ".join(sorted(unknown))
            )

        return errors

    # -----------------------------------------
    # OUTPUT TYPE DETECTION
    # -----------------------------------------

    def _detect_output_type(self, result):

        content_fields = {
            "hook",
            "script",
            "caption",
            "cta",
            "hashtags",
        }

        product_fields = {
            "product_name",
            "tagline",
            "description",
            "target_audience",
            "product_structure",
            "prompt_pack",
            "notion_workspace",
            "automation_blueprints",
            "pricing",
            "marketing_angle",
            "launch_strategy",
        }

        keys = set(result.keys())

        if keys & content_fields:
            return "content"

        if keys & product_fields:
            return "product"

        return None

    # -----------------------------------------
    # ERROR OUTPUT DETECTION
    # -----------------------------------------

    def _is_error_output(self, result):

        error_keys = {
            "raw_content",
            "raw_response",
            "status",
            "message",
            "error",
        }

        if "raw_content" in result:
            return True

        if "raw_response" in result:
            return True

        if (
            result.get("status") == "ERROR"
            or "error" in result
        ):
            return True

        return False

    # -----------------------------------------
    # TEXT FLATTENING
    # -----------------------------------------

    def _flatten_to_text(self, value):

        if isinstance(value, dict):

            return " ".join(
                self._flatten_to_text(item)
                for item in value.values()
            )

        if isinstance(value, list):

            return " ".join(
                self._flatten_to_text(item)
                for item in value
            )

        return str(value)

    # -----------------------------------------
    # QUALITY SCORE
    # -----------------------------------------

    def _calculate_score(
        self,
        result,
        warnings
    ):

        score = 100

        score -= len(warnings) * 10

        output_type = self._detect_output_type(result)

        if output_type == "content":

            required = [
                "hook",
                "script",
                "caption",
                "cta",
            ]

            completed = sum(
                bool(result.get(field))
                for field in required
            )

            score -= (
                (len(required) - completed)
                * 10
            )

        elif output_type == "product":

            required = [
                "product_name",
                "description",
                "target_audience",
                "product_structure",
            ]

            completed = sum(
                bool(result.get(field))
                for field in required
            )

            score -= (
                (len(required) - completed)
                * 10
            )

        return max(
            0,
            min(100, score)
        )

    # -----------------------------------------
    # FAILURE RESPONSE
    # -----------------------------------------

    def _failure(
        self,
        errors,
        warnings=None
    ):

        return {
            "status": "NEEDS_REVIEW",
            "valid": False,
            "errors": errors,
            "warnings": warnings or [],
            "quality_score": 0
        }