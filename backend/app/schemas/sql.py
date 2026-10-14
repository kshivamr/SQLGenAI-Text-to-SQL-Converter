from pydantic import BaseModel

class SQLRequest(BaseModel):
    question: str