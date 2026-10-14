from fastapi import APIRouter
from backend.app.schemas.sql import SQLRequest
from backend.app.services.model_service import generate_sql
from backend.app.services.sql_validator import validate_sql
from backend.app.services.sql_executor import execute_sql

router = APIRouter()

@router.post("/generate")
def generate(request: SQLRequest):
    sql = generate_sql(request.question)

    validated_sql = validate_sql(sql)

    results = execute_sql(validated_sql)

    return {
        "question": request.question,
        "sql": validated_sql,
        "results": results
    }