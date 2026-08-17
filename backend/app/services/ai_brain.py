import os
import time
from dotenv import load_dotenv

try:
    from google import genai
except ImportError:  # pragma: no cover - handled as a configuration error at runtime
    genai = None

load_dotenv()


class AIBrain:
    """
    CreatorOS Central AI Brain

    Handles communication between AI Employees
    and the Gemini API.
    """

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is missing from the .env file."
            )

        if genai is None:
            raise RuntimeError(
                "The google-genai package is not installed. "
                "Install backend requirements before generating content."
            )

        self.client = genai.Client(
            api_key=api_key
        )

        # Use the model that is available to your API key.
        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.1-flash-lite"
        )

        self.max_retries = 2
        self.retry_delay = 5

    def think(
        self,
        system_prompt: str,
        user_prompt: str
    ):

        prompt = f"""
SYSTEM:
{system_prompt}

USER:
{user_prompt}
"""

        last_error = None

        for attempt in range(self.max_retries):

            try:

                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt
                )

                if not response or not response.text:
                    raise RuntimeError(
                        "Gemini returned an empty response."
                    )

                return response.text

            except Exception as error:

                last_error = error

                error_text = str(error)

                print(
                    f"Gemini request failed "
                    f"(attempt {attempt + 1}/"
                    f"{self.max_retries}): {error}"
                )

                # -----------------------------------------
                # QUOTA ERROR
                # -----------------------------------------

                if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:

                    raise RuntimeError(
                        "Gemini API quota exceeded. "
                        "CreatorOS could not complete this AI task. "
                        "Please wait for the quota to reset or "
                        "use a Gemini API billing plan with higher limits."
                    ) from error

                # -----------------------------------------
                # MODEL ERROR
                # -----------------------------------------

                if "404" in error_text or "NOT_FOUND" in error_text:

                    raise RuntimeError(
                        f"Gemini model '{self.model}' is unavailable "
                        "for this API key. "
                        "Set GEMINI_MODEL in your .env file to an "
                        "available model."
                    ) from error

                # -----------------------------------------
                # TEMPORARY SERVER ERROR
                # -----------------------------------------

                if (
                    "503" in error_text
                    or "UNAVAILABLE" in error_text
                ):

                    if attempt < self.max_retries - 1:
                        time.sleep(self.retry_delay)
                        continue

                    raise RuntimeError(
                        "Gemini service is temporarily unavailable. "
                        "Please try again later."
                    ) from error

                # -----------------------------------------
                # OTHER ERROR
                # -----------------------------------------

                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)

        raise RuntimeError(
            "Gemini request failed after all retry attempts."
        ) from last_error