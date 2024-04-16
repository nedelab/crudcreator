from pydantic import BaseModel
from typing import Optional

class _BulkErrorModel(BaseModel):
    http_status: int
    detail: str

class BulkErrorModel(BaseModel):
    detail: list[_BulkErrorModel]