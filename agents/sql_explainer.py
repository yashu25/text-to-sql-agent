import os
import requests

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

def explain_sql(sql):
    prompt = f"""
You are a senior data analyst.

Explain the following SQL query in simple business-friendly language.
Do NOT repeat the SQL.
Explain:
- What data is being used
- What calculation is happening
- What the result represents

SQL:
{sql}
"""

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "mistralai/mistral-7b-instruct",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3
        }
    )

    data = response.json()
    if "choices" not in data:
        return "Could not generate explanation."

    return data["choices"][0]["message"]["content"]

