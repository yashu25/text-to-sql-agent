def validate_sql(sql):
    forbidden = ["delete", "update", "insert", "drop", "alter"]
    for word in forbidden:
        if word in sql.lower():
            raise ValueError("Unsafe SQL detected.")
    return sql

