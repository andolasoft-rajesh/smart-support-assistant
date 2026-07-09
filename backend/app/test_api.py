from google import genai

client = genai.Client(
    api_key="PASTE_YOUR_API_KEY_HERE"
)

try:
    models = client.models.list()

    for m in models:
        print(m.name)

except Exception as e:
    print(e)
