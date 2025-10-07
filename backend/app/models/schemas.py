from pydantic import BaseModel
from typing import List, Optional


class UploadResponse(BaseModel):
    doc_id: str
    chunk_count: int
    filename: str


class QARequest(BaseModel):
    question: str
    doc_id: str
    top_k: int = 5


class Source(BaseModel):
    id: str
    score: float
    chunk: Optional[int]
    filename: Optional[str]


class QAResponse(BaseModel):
    answer: str
    sources: List[Source]
    used_chunks: int
