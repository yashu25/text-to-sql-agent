# 🗄️ Text-to-SQL Agent

> Ask questions in plain English — get SQL queries and results instantly

[![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.x-black?logo=flask)](https://flask.palletsprojects.com)
[![SQLite](https://img.shields.io/badge/SQLite-3-blue?logo=sqlite)](https://sqlite.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## 🤔 What is this?

Non-technical users waste hours asking developers for simple data queries. **Text-to-SQL Agent** eliminates that — type a question in plain English, get the SQL query, execute it, and see results instantly.

Upload your Excel file, ask anything about your data, and the agent handles the rest.

---

## 🤖 How It Works — 3-Agent Pipeline
```
📝 SQL Generator  →  ✅ SQL Validator  →  💬 SQL Explainer
```

| Agent | Role |
|-------|------|
| 📝 **SQL Generator** | Converts natural language question into a SQL query using LLM |
| ✅ **SQL Validator** | Sanitizes and validates the SQL — removes bad syntax, named params, reserved keywords |
| 💬 **SQL Explainer** | Explains what the SQL query does in plain English |

---

## ✨ Features

- **Natural language to SQL** — no SQL knowledge needed
- **Excel upload** — upload any `.xlsx` file, it auto-imports to SQLite
- **Multi-sheet support** — handles Excel files with multiple sheets
- **SQL guardrails** — validates and sanitizes before execution
- **Plain English explanation** — explains what the query does
- **Built-in sample DB** — works out of the box, no setup needed
- **Web UI** — clean Flask interface, runs in browser

---

## 🚀 Quick Start

### Step 1 — Clone the repo
```bash
git clone https://github.com/yashu25/text-to-sql-agent.git
cd text-to-sql-agent
```

### Step 2 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Run the app
```bash
python app.py
```

Open `http://localhost:5001` in your browser.

---

## 📖 How to Use

**Option A — Use the sample database**
The app comes with a built-in `sample.db` — just start asking questions immediately.

**Option B — Upload your own Excel file**
1. Click **Upload Excel** and select your `.xlsx` file
2. The app imports all sheets as database tables automatically
3. Start asking questions about your data

**Example questions:**
- *"Show me the top 10 customers by revenue"*
- *"How many orders were placed last month?"*
- *"What is the average order value by region?"*
- *"List all products where stock is below 50"*

---

## 📁 Project Structure
```
text-to-sql-agent/
├── app.py                  ← Flask app, main routes, Excel importer
├── agents/
│   ├── sql_generator.py    ← LLM-powered SQL generation
│   ├── sql_validator.py    ← SQL sanitization & validation
│   └── sql_explainer.py    ← Plain English explanation of SQL
├── db/
│   ├── sample.db           ← Sample SQLite database
│   └── setup_db.py         ← DB initialization script
├── templates/
│   └── index.html          ← Web UI
├── static/                 ← CSS & JS assets
├── uploads/                ← Uploaded Excel files (auto-created)
└── requirements.txt
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask |
| Database | SQLite |
| Data Import | Pandas, openpyxl |
| AI / LLM | OpenAI API (via agents) |
| Frontend | HTML, CSS, Jinja2 templates |

---

## 🔒 SQL Safety

The app includes multiple layers of SQL protection:

- **Hard sanitizer** — strips markdown code fences, named parameters, stray colons
- **Reserved keyword guard** — blocks queries using SQL reserved words as table names
- **Positional clause cleanup** — removes `ORDER BY 1`, `GROUP BY 1` style clauses
- **Try/except execution** — catches and surfaces SQL errors gracefully

---


*Built with ❤️ · Ask your data anything*
