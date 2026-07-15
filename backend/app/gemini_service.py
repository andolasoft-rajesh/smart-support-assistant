import os
from dotenv import load_dotenv
from google import genai
from groq import Groq

load_dotenv()

# Gemini client (Embeddings only)
gemini_client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Groq client (Answer generation)
groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def ask_gemini(prompt: str):
    """
    Generates the final answer using Groq.
    Function name is kept the same so you don't have to
    change the rest of your project.
    """

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content


def create_embedding(text: str):
    """
    Embeddings still come from Gemini.
    """

    response = gemini_client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
        config={
            "output_dimensionality": 768
        }
    )

    return response.embeddings[0].values