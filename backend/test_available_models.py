"""Manual Gemini model discovery; not part of the deterministic test suite."""

import os

from dotenv import load_dotenv
from google import genai


models_to_test = [
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
    "gemini-flash-latest",
    "gemini-flash-lite-latest",
    "gemini-3-flash-preview",
    "gemini-3.1-flash-lite",
]


def main():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured.")

    client = genai.Client(api_key=api_key)

    for model in models_to_test:
        print("\n" + "=" * 60)
        print("TESTING:", model)
        print("=" * 60)

        try:
            response = client.models.generate_content(
                model=model,
                contents="Reply with exactly: MODEL WORKS",
            )
            print("SUCCESS:")
            print(response.text)
        except Exception as error:
            print("FAILED:")
            print(error)


if __name__ == "__main__":
    main()
