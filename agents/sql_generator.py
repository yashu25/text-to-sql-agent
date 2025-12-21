import os
import requests

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

def generate_sql(question, schema):
    if not OPENROUTER_API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY not set")

    prompt = f"""
You are an expert data analyst.

Database schema:
{schema}

Rules:
- Generate ONLY a SELECT SQL query
- No explanations
- No markdown
- Use correct column names

User question:
{question}

Return only SQL.
"""

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://localhost",
            "X-Title": "Text-to-SQL-Agent"
        },
        json={
            "model": "mistralai/mistral-7b-instruct",
            "messages": [
                {"role": "system", "content": "You generate SQL queries."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0
        },
        timeout=30
    )

    data = response.json()
    if "choices" not in data:
        raise RuntimeError(f"OpenRouter API Error: {data}")

    return data["choices"][0]["message"]["content"].strip()
