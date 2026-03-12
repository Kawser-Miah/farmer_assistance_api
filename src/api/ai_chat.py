from fastapi import APIRouter
from pydantic import BaseModel
from src.services.ai_chat.ai_chat_base import chat_with_ai
from src.core.config import settings


router = APIRouter(
    prefix=settings.ai_chat_prefix,
    tags=["AI Chat"]
)

class ChatRequest(BaseModel):

    query: str


@router.post("/chat")
async def ai_chat(request: ChatRequest):

    response = chat_with_ai(request.query)

    return response