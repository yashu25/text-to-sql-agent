import os
import requests

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

def generate_sql(question, schema):
    if not OPENROUTER_API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY not set")

    prompt = f"""
You are an expert SQLite SQL generator.

Database schema:
{schema}

CRITICAL SQLITE RULES (MUST FOLLOW):
- Use ONLY table and column names from the schema
- If a column name contains spaces, hyphens, or brackets, ALWAYS wrap it in double quotes
  Examples:
  - "Price per Unit (in INR)"
  - "Order-ID"
  - "Sub Category"
- NEVER use positional references like GROUP BY 1 or ORDER BY 1
- ALWAYS use explicit column names in GROUP BY and ORDER BY
- NEVER use ':' or named parameters
- Generate ONLY one valid SQLite SELECT query
- No explanations
- No markdown
- No comments
- Output must run directly in sqlite3 without modification

User question:
{question}

Return ONLY the SQL query.
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
                {"role": "system", "content": "You generate STRICT SQLite-compatible SQL only."},
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
