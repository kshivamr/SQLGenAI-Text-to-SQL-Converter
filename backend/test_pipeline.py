import sys

sys.path.append("backend")

from app.services.model_service import generate_sql
from app.services.sql_executor import execute_sql

question = "Show the top 5 employees with the highest salary."

sql = generate_sql(question)

print("Question:")
print(question)

print("\nGenerated SQL:")
print(sql)

results = execute_sql(sql)

print("\nResults:")

for row in results:
    print(row)