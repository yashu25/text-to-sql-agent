import pandas as pd
from flask import Flask, request, render_template
import sqlite3, os

from agents.sql_generator import generate_sql
from agents.sql_validator import validate_sql
from agents.explainer import explain_result
from agents.sql_explainer import explain_sql

if not os.path.exists("db/sample.db"):
    import db.setup_db

app = Flask(__name__)

SCHEMA = "sales(id, region, product, revenue, year, month)"
def import_excel_to_db(file_path):
    conn = sqlite3.connect("db/sample.db")
    xls = pd.ExcelFile(file_path)

    schema_lines = []

    for sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet)
        table = sheet.lower()
        df.to_sql(table, conn, if_exists="replace", index=False)
        schema_lines.append(f"{table}({', '.join(df.columns)})")

    conn.close()
    return "\n".join(schema_lines)
schema_text = ""

@app.route("/", methods=["GET", "POST"])
def home():
    global schema_text
    sql = result = explanation = None

    # Excel upload
    if "excel" in request.files:
        file = request.files["excel"]
        if file.filename.endswith(".xlsx"):
            path = os.path.join("uploads", file.filename)
            file.save(path)
            schema_text = import_excel_to_db(path)

    # Question submit
    if request.method == "POST" and "question" in request.form:
        q = request.form["question"]

        sql = generate_sql(q, schema_text)
        sql = sql.replace("```sql", "").replace("```", "").strip()
        sql = validate_sql(sql)

        conn = sqlite3.connect("db/sample.db")
        cur = conn.cursor()
        cur.execute(sql)
        if " table " in sql.lower():
            raise ValueError("Invalid SQL generated: reserved keyword 'table' used")

        result = cur.fetchall()
        conn.close()

        explanation = explain_sql(sql)

    return render_template(
        "index.html",
        schema=schema_text,
        sql=sql,
        result=result,
        explanation=explanation
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

