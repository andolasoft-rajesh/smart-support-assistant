"""
Author: Priya Dash
Feature: Document Summary
"""

SUMMARY_PROMPT = """
You are an AI assistant.

Read the document provided by the user.

Return ONLY valid JSON.

Do not write explanations.
Do not use markdown.
Do not wrap the JSON in ```.

The JSON must exactly follow this schema:

{
  "title": "string",
  "summary": "string",
  "key_points": [
    "string",
    "string",
    "string"
  ]
}
"""
