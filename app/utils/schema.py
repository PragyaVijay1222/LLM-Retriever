from pydantic import BaseModel
from typing import List, Optional

class QueryRequest(BaseModel):
    documents: str
    questions: List[str]

class AnswerResponse(BaseModel):
    question: str
    answer: str
    conditions: List[str]
    source_clauses: List[dict]