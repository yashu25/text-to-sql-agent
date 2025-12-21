import os
import requests

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

def generate_sql(question, schema):
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is not set")

    prompt = f"""
You are an expert data analyst.

Database schema:
{schema}

Rules:
- Generate ONLY a SELECT SQL query
- Do not use DELETE, UPDATE, INSERT, DROP
- Use correct column names
- Do not add explanations or markdown

User question:
{question}

Return only SQL.
"""

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "system", "content": "You generate SQL queries."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0
        },
        timeout=30
    )

    data = response.json()

    # 🔴 CRITICAL SAFETY CHECK
    if "choices" not in data:
        raise RuntimeError(f"Groq API Error: {data}")

    sql = data["choices"][0]["message"]["content"]
    return sql.strip()
