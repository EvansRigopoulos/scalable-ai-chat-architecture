import json
from typing import TypedDict

from fastapi import APIRouter, HTTPException
from langgraph.graph import state
from langgraph.types import Command

from app.services.chat_service import ChatService
from app.api.schemas import ChatResponse, ChatRequest, ReviewUpdate
from app.services.graph_service import GraphService

router = APIRouter()
graph_service = GraphService()
chat_service = ChatService(graph_service)

class HumanReviewState(TypedDict):
    text: str
@router.get("/health")
async def health():
    return {"status": "ok"}


@router.post("/chat",response_model=ChatResponse)
async def chat(request: ChatRequest):
    response_text =  await chat_service.generate_response(request.user_id,request.message,request.session_id)
    return ChatResponse(response=response_text)










