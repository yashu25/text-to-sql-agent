import os
import re
import sqlite3
import pandas as pd
from flask import Flask, request, render_template

from agents.sql_generator import generate_sql
from agents.sql_validator import validate_sql
from agents.sql_explainer import explain_sql

# -------------------------
# App & folders
# -------------------------
app = Flask(__name__)

os.makedirs("uploads", exist_ok=True)
os.makedirs("db", exist_ok=True)

# -------------------------
# Ensure DB exists
# -------------------------
if not os.path.exists("db/sample.db"):
    import db.setup_db

# -------------------------
# Excel → SQLite importer
# -------------------------
def import_excel_to_db(file_path):
    conn = sqlite3.connect("db/sample.db")
    xls = pd.ExcelFile(file_path)

    schema_lines = []

    for sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet)

        table = sheet.lower().replace(" ", "_")
        if table == "table":
            table = "data_table"

        df.to_sql(table, conn, if_exists="replace", index=False)
        schema_lines.append(f"{table}({', '.join(df.columns)})")

    conn.close()
    return "\n".join(schema_lines)

schema_text = ""

# -------------------------
# Main route
# -------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    global schema_text
    sql = result = explanation = None

    # ---- Excel upload ----
    if "excel" in request.files:
        file = request.files["excel"]
        if file and file.filename.endswith(".xlsx"):
            path = os.path.join("uploads", file.filename)
            file.save(path)
            schema_text = import_excel_to_db(path)

    # ---- Question submit ----
    if request.method == "POST" and "question" in request.form:
        q = request.form["question"]

        # Generate SQL
        sql = generate_sql(q, schema_text)
        sql = sql.replace("```sql", "").replace("```", "").strip()
        sql = validate_sql(sql)

        # ---- SQL GUARDRAILS ----
        if " table " in sql.lower():
            raise ValueError("Invalid SQL generated: reserved keyword 'table' used")

        # SQLite does NOT support GROUP BY 1 / ORDER BY 1
        sql = re.sub(r'GROUP BY\s+1', '', sql, flags=re.IGNORECASE)
        sql = re.sub(r'ORDER BY\s+1', '', sql, flags=re.IGNORECASE)

        print("🟢 FINAL SQL:", sql)

        # ---- Execute SQL ----
        conn = sqlite3.connect("db/sample.db")
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        conn.close()

        # Explain SQL
        explanation = explain_sql(sql)

    return render_template(
        "index.html",
        schema=schema_text,
        sql=sql,
        result=result,
        explanation=explanation
    )

# -------------------------
# Run
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
