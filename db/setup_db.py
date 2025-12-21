import sqlite3

conn = sqlite3.connect("sample.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY,
    region TEXT,
    product TEXT,
    revenue INTEGER,
    year INTEGER,
    month TEXT
)
""")

data = [
    ("North", "Protein Powder", 120000, 2024, "Jan"),
    ("South", "Creatine", 95000, 2024, "Jan"),
    ("North", "Creatine", 110000, 2025, "Feb"),
    ("West", "Protein Powder", 70000, 2025, "Jan"),
    ("South", "Protein Powder", 130000, 2025, "Feb"),
]

cur.executemany(
    "INSERT INTO sales (region, product, revenue, year, month) VALUES (?, ?, ?, ?, ?)",
    data
)

conn.commit()
conn.close()
print("✅ Database ready.")

