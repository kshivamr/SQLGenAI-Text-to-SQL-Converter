import sys

sys.path.append("backend")

from app.services.sql_executor import execute_sql

sql = """
SELECT name, salary
FROM employees
ORDER BY salary DESC
LIMIT 5
"""

results = execute_sql(sql)

print("Results:")

for row in results:
    print(row)