from pydantic import BaseModel

class ErrorModel(BaseModel):
    detail: str