from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

models_to_test = [
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
    "gemini-flash-latest",
    "gemini-flash-lite-latest",
    "gemini-3-flash-preview",
    "gemini-3.1-flash-lite",
]

for model in models_to_test:

    print("\n" + "=" * 60)
    print("TESTING:", model)
    print("=" * 60)

    try:

        response = client.models.generate_content(
            model=model,
            contents="Reply with exactly: MODEL WORKS"
        )

        print("SUCCESS:")
        print(response.text)

    except Exception as error:

        print("FAILED:")
        print(error)