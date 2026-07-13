import logging
from typing import List, Dict, Any

from fastapi import APIRouter
from pydantic import BaseModel

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/chat", tags=["Chat"])

try:
    from backend.services.agent import agent_service
    AGENT_AVAILABLE = True
except ImportError:
    AGENT_AVAILABLE = False
    logger.warning("Agent service not available")


class ChatRequest(BaseModel):
    message: str
    history: List[Dict[str, str]] = []


class ChatResponse(BaseModel):
    response: str


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not AGENT_AVAILABLE:
        return ChatResponse(response="AI agent is not configured. Set LLM_API_KEY in environment.")

    response = await agent_service.chat(
        message=request.message,
        history=request.history
    )
    return ChatResponse(response=response)