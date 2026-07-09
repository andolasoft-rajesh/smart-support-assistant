import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

print("USING KEY:", api_key[:10] if api_key else "NO KEY")

client = genai.Client(api_key=api_key)


def ask_llm(prompt: str):

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )

    return response.text