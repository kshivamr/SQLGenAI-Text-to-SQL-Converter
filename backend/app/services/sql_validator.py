import re

def validate_sql(sql):
    sql = sql.strip()

    if not sql.lower().startswith("select"):
        raise ValueError("Only SELECT queries are allowed.")

    forbidden = [
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "truncate",
        "create"
    ]

    for keyword in forbidden:
        if re.search(rf"\b{keyword}\b", sql, re.IGNORECASE):
            raise ValueError(f"Forbidden SQL operation: {keyword}")

    return sql