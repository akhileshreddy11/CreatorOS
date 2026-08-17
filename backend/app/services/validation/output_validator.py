import re


class OutputValidator:
    """
    CreatorOS Output Validator

    Validates AI employee output before it is
    accepted by the Mission Execution Engine.

    Checks:
    - Unsupported guarantees
    - Unsupported income claims
    - Unsupported performance claims
    - Fabricated personal experiences
    - Numeric performance claims
    - Basic content quality
    - Product output quality
    """

    def __init__(self):

        # Claims that should never be presented as facts
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

        # Numeric claims that may require verification.
        # These are warnings rather than automatic failures.
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
                errors=["AI returned no output."]
            )

        if not isinstance(result, dict):

            return self._failure(
                errors=[
                    "AI output must be a JSON object."
                ]
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
        # CONTENT VALIDATION
        # -----------------------------------------

        if self._looks_like_content(result):

            required_fields = [
                "hook",
                "script",
                "caption",
                "cta",
            ]

            missing = [
                field
                for field in required_fields
                if not result.get(field)
            ]

            if missing:

                errors.append(
                    "Missing required content fields: "
                    + ", ".join(missing)
                )

        # -----------------------------------------
        # PRODUCT VALIDATION
        # -----------------------------------------

        if self._looks_like_product(result):

            required_fields = [
                "product_name",
                "description",
                "target_audience",
                "product_structure",
            ]

            missing = [
                field
                for field in required_fields
                if not result.get(field)
            ]

            if missing:

                errors.append(
                    "Missing required product fields: "
                    + ", ".join(missing)
                )

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
    # HELPERS
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

    def _looks_like_content(self, result):

        content_fields = [
            "hook",
            "script",
            "caption",
            "cta",
            "hashtags",
        ]

        return any(
            field in result
            for field in content_fields
        )

    def _looks_like_product(self, result):

        product_fields = [
            "product_name",
            "product_structure",
            "notion_workspace",
            "automation_blueprints",
        ]

        return any(
            field in result
            for field in product_fields
        )

    def _calculate_score(
        self,
        result,
        warnings
    ):

        score = 100

        score -= len(warnings) * 10

        if self._looks_like_content(result):

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

        if self._looks_like_product(result):

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