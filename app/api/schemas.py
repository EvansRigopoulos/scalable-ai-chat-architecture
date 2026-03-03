from typing import TypedDict

from pydantic import BaseModel

class ChatRequest(BaseModel):
    user_id: int
    message: str
    session_id: str

class ChatResponse(BaseModel):
    response: str

class ReviewUpdate(BaseModel):
    session_id: str
    approved_text: str