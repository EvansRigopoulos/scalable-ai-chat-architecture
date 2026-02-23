from fastapi import APIRouter
from app.services.chat_service import ChatService
from app.api.schemas import ChatResponse, ChatRequest

router = APIRouter()
chat_service = ChatService()
@router.get("/health")
async def health():
    return {"status": "ok"}


@router.post("/chat",response_model=ChatResponse)
async def chat(request: ChatRequest):
    response_text =  await chat_service.generate_response(request.user_id,request.message)
    return ChatResponse(response=response_text)

