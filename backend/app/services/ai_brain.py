import os
import time

from dotenv import load_dotenv

try:
    from google import genai
    from google.genai import types
except ImportError:  # pragma: no cover
    genai = None
    types = None

load_dotenv()


class AIBrain:
    """
    CreatorOS Central AI Brain.

    Responsible for communicating with the Gemini API while providing:

    - API-key validation
    - Configurable model selection
    - Request timeout protection
    - Retry handling
    - Quota detection
    - Model availability detection
    - Temporary service-error handling
    - Safe diagnostic messages

    All CreatorOS AI employees use this class.
    """

    DEFAULT_MODEL = "gemini-3.1-flash-lite"

    # Gemini SDK timeout is specified in milliseconds.
    DEFAULT_TIMEOUT_MS = 30000

    DEFAULT_MAX_RETRIES = 2
    DEFAULT_RETRY_DELAY = 2

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is missing from the .env file."
            )

        if genai is None or types is None:
            raise RuntimeError(
                "The google-genai package is not installed. "
                "Install backend requirements before generating content."
            )

        self.model = os.getenv(
            "GEMINI_MODEL",
            self.DEFAULT_MODEL,
        )

        self.timeout_ms = self._get_int_env(
            "GEMINI_TIMEOUT_MS",
            self.DEFAULT_TIMEOUT_MS,
        )

        self.max_retries = self._get_int_env(
            "GEMINI_MAX_RETRIES",
            self.DEFAULT_MAX_RETRIES,
        )

        self.retry_delay = self._get_float_env(
            "GEMINI_RETRY_DELAY",
            self.DEFAULT_RETRY_DELAY,
        )

        if self.timeout_ms < 1000:
            raise ValueError(
                "GEMINI_TIMEOUT_MS must be at least 1000 milliseconds."
            )

        if self.max_retries < 1:
            raise ValueError(
                "GEMINI_MAX_RETRIES must be at least 1."
            )

        print(
            f"[AIBrain] Model: {self.model} | "
            f"Timeout: {self.timeout_ms}ms | "
            f"Retries: {self.max_retries}"
        )

        self.client = genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(
                timeout=self.timeout_ms
            ),
        )

    # ============================================================
    # ENVIRONMENT HELPERS
    # ============================================================

    @staticmethod
    def _get_int_env(name, default):
        value = os.getenv(name)

        if value is None or not value.strip():
            return default

        try:
            return int(value)
        except ValueError:
            raise ValueError(
                f"{name} must be an integer. "
                f"Received: {value!r}"
            )

    @staticmethod
    def _get_float_env(name, default):
        value = os.getenv(name)

        if value is None or not value.strip():
            return default

        try:
            return float(value)
        except ValueError:
            raise ValueError(
                f"{name} must be a number. "
                f"Received: {value!r}"
            )

    # ============================================================
    # ERROR CLASSIFICATION
    # ============================================================

    @staticmethod
    def _is_quota_error(error_text):
        upper = error_text.upper()

        return (
            "429" in error_text
            or "RESOURCE_EXHAUSTED" in upper
            or "QUOTA" in upper
        )

    @staticmethod
    def _is_model_error(error_text):
        upper = error_text.upper()

        return (
            "404" in error_text
            or "NOT_FOUND" in upper
            or "MODEL_NOT_FOUND" in upper
        )

    @staticmethod
    def _is_temporary_error(error_text):
        upper = error_text.upper()

        return (
            "503" in error_text
            or "UNAVAILABLE" in upper
            or "DEADLINE" in upper
            or "TIMEOUT" in upper
            or "TIMED OUT" in upper
            or "504" in error_text
        )

    # ============================================================
    # SAFE ERROR MESSAGE
    # ============================================================

    @staticmethod
    def _safe_error(error):
        """
        Prevent API keys or credentials from appearing in logs.
        """

        message = str(error).strip()

        if not message:
            return error.__class__.__name__

        # Google API key patterns.
        import re

        message = re.sub(
            r"AIza[0-9A-Za-z_-]+",
            "[REDACTED_API_KEY]",
            message,
        )

        # Generic API-key patterns.
        message = re.sub(
            r"(?i)(api[_ -]?key\s*[=:]\s*)[^\s,;]+",
            r"\1[REDACTED]",
            message,
        )

        return message[:1500]

    # ============================================================
    # MAIN AI FUNCTION
    # ============================================================

    def think(
        self,
        system_prompt: str,
        user_prompt: str,
    ):
        """
        Send a request to Gemini.

        Returns:
            str: Gemini generated text.

        Raises:
            RuntimeError: when the request cannot safely complete.
        """

        prompt = f"""
SYSTEM:
{system_prompt}

USER:
{user_prompt}
"""

        last_error = None

        for attempt in range(
            1,
            self.max_retries + 1,
        ):
            start_time = time.perf_counter()

            try:
                print(
                    f"[AIBrain] Gemini request "
                    f"{attempt}/{self.max_retries} started..."
                )

                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                )

                elapsed = time.perf_counter() - start_time

                print(
                    f"[AIBrain] Gemini request completed "
                    f"in {elapsed:.2f}s."
                )

                if not response:
                    raise RuntimeError(
                        "Gemini returned an empty response object."
                    )

                text = getattr(
                    response,
                    "text",
                    None,
                )

                if not text:
                    raise RuntimeError(
                        "Gemini returned an empty text response."
                    )

                return text.strip()

            except Exception as error:
                last_error = error

                elapsed = time.perf_counter() - start_time
                error_text = str(error)
                safe_error = self._safe_error(error)

                print(
                    f"[AIBrain] Gemini request failed "
                    f"after {elapsed:.2f}s "
                    f"(attempt {attempt}/{self.max_retries}): "
                    f"{safe_error}"
                )

                # ------------------------------------------------
                # QUOTA
                # ------------------------------------------------

                if self._is_quota_error(error_text):
                    raise RuntimeError(
                        "Gemini API quota exceeded. "
                        "CreatorOS could not complete this AI task. "
                        "Please wait for the quota to reset or "
                        "use a Gemini API billing plan with higher limits."
                    ) from error

                # ------------------------------------------------
                # MODEL
                # ------------------------------------------------

                if self._is_model_error(error_text):
                    raise RuntimeError(
                        f"Gemini model '{self.model}' is unavailable "
                        "for this API key. "
                        "Set GEMINI_MODEL in your .env file to an "
                        "available model."
                    ) from error

                # ------------------------------------------------
                # TEMPORARY / TIMEOUT
                # ------------------------------------------------

                if self._is_temporary_error(error_text):

                    if attempt < self.max_retries:
                        print(
                            f"[AIBrain] Temporary Gemini failure. "
                            f"Retrying in {self.retry_delay}s..."
                        )

                        time.sleep(self.retry_delay)
                        continue

                    raise RuntimeError(
                        "Gemini request timed out or the service "
                        "was temporarily unavailable after "
                        f"{self.max_retries} attempts."
                    ) from error

                # ------------------------------------------------
                # UNKNOWN ERROR
                # ------------------------------------------------

                if attempt < self.max_retries:
                    print(
                        f"[AIBrain] Retrying in "
                        f"{self.retry_delay}s..."
                    )

                    time.sleep(self.retry_delay)
                    continue

        raise RuntimeError(
            "Gemini request failed after all retry attempts: "
            f"{self._safe_error(last_error)}"
        ) from last_error