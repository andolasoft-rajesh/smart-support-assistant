SUMMARY_PROMPT = """
Summarize the following document.

Return ONLY valid JSON.

Example:

{
    "summary": "Short summary",
    "key_points": [
        "Point 1",
        "Point 2",
        "Point 3"
    ]
}

Document:
"""