import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env")

client = Groq(api_key=api_key)


def ask_llm(prompt: str):
    try:
        print("\n========== PROMPT SENT TO GROQ ==========")
        print(prompt)
        print("=========================================\n")

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": """
You are a helpful AI assistant.

Rules:
- Answer normally for general questions.
- Use provided document context only when it is relevant.
- Never return an empty answer.
"""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_tokens=1024
        )

        # Debug Groq complete response
        print("======================")
        print("GROQ FULL RESPONSE:")
        print(response)
        print("======================")

        answer = response.choices[0].message.content

        print("======================")
        print("GROQ TEXT RESPONSE:")
        print(answer)
        print("======================")

        if not answer or answer.strip() == "":
            return "I could not generate an answer. Please try again."

        return answer.strip()

    except Exception as e:
        print("Groq Error:", e)
        raise