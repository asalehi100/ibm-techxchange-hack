"""Prompt templates for AI model interactions."""

meeting_prompt = """
You are an AI assistant that extracts meeting details only from valid meeting requests.
Extract only structured details from this meeting request. Output as JSON:
{{
  "participants": [...] only take names from input don't add extra names,
  "date": "..." (Convert text to date format: DD-MM-YYYY)),
  "time": "...",
  "topic": "..."
}}
Use explicit formats:
- Date: YYYY-MM-DD use default year as 2025
- Time: HH:MM in 24-hr format (UTC preferred)
Meeting request: "Set a meeting with Alice and Bob next Tuesday at 11am to discuss Q2 hiring."Only return the final JSON. **Do not include any explanation, examples, or extra responses.**
Request: "{request}"
Return as JSON.
"""

