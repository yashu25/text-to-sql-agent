import os
import requests

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

def generate_sql(question, schema):
    prompt = f"""
You are an expert data analyst.

Database schema:
{schema}

Rules:
- Generate ONLY a SELECT SQL query
- Do not use DELETE, UPDATE, INSERT, DROP
- Use correct column names
- Do not explain anything

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
        }
    )
    return response.json()["choices"][0]["message"]["content"]

