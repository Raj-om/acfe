from pydantic import BaseModel
from typing import Generic, TypeVar, List

T = TypeVar("T")

class Pagination(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int

class ErrorResponse(BaseModel):
    code: int
    message: str

class HealthResponse(BaseModel):
    status: str
    db_connected: bool
