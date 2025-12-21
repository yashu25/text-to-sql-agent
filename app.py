from flask import Flask, request, render_template
import sqlite3, os

from agents.sql_generator import generate_sql
from agents.sql_validator import validate_sql
from agents.explainer import explain_result

if not os.path.exists("db/sample.db"):
    import db.setup_db

app = Flask(__name__)

SCHEMA = "sales(id, region, product, revenue, year, month)"

@app.route("/", methods=["GET","POST"])
def home():
    sql = result = None

    if request.method == "POST":
        q = request.form["question"]
        sql = generate_sql(q, SCHEMA)
        sql = validate_sql(sql)

        conn = sqlite3.connect("db/sample.db")
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        conn.close()

    return render_template("index.html", sql=sql, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

