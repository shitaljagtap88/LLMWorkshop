import os

from google import genai

api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
if not api_key:
    raise RuntimeError(
        "Set GEMINI_API_KEY or GOOGLE_API_KEY before running this script."
    )

client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents="Say Hello World",
)

print(response.text)
