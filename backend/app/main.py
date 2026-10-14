from fastapi import FastAPI
from backend.app.routes.sql import router as sql_router

app = FastAPI(title="SQLGenAI")

app.include_router(
    sql_router,
    prefix="/sql",
    tags=["SQL"]
)

@app.get("/")
def root():
    return {"message": "SQLGenAI API is running"}