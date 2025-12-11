from pydantic import BaseModel
from typing import List

class QueryRequest(BaseModel):
    query: str

class CourseItem(BaseModel):
    subject: str
    level: str
    reviews: int
    price: str
    duration: str
    url: str

class QueryResponse(BaseModel):
    items: List[CourseItem]
    query: str