from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID, uuid4
from datetime import datetime


from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID, uuid4
from datetime import datetime


class ChatMessage(BaseModel):
    role: str = Field(..., examples=["user", "assistant"])
    content: str = Field(..., examples=["What is crop rotation?"])
    timestamp: str = Field(..., examples=["2024-03-22T10:30:00Z"])


class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000, examples=["How can I treat powdery mildew in cucumber?"])
    conversation_id: Optional[UUID] = Field(None, examples=[uuid4()])
    conversation_history: Optional[List[ChatMessage]] = Field(None, description="Client's current conversation history (optional)")


class ChatSource(BaseModel):
    content: str = Field(..., examples=["Powdery mildew appears as white powder on leaves."])


class ChatResponse(BaseModel):
    answer: str = Field(..., examples=["Use sulfur-based fungicide and improve airflow around plants."])
    sources: list[ChatSource] = Field(default_factory=list)
    conversation_id: UUID = Field(..., examples=[uuid4()])
    conversation_history: List[ChatMessage] = Field(default_factory=list, description="Updated conversation history for display")
    conversation_title: Optional[str] = Field(None, description="AI-generated conversation title", examples=["Tomato Disease Treatment"])


class ConversationPair(BaseModel):
    question: str = Field(..., examples=["What is crop rotation?"])
    answer: str = Field(..., examples=["Crop rotation is the practice of growing different crops..."])
    timestamp: str = Field(..., examples=["2024-03-22T10:30:00Z"])


class ConversationHistory(BaseModel):
    conversation_id: UUID = Field(..., examples=[uuid4()])
    pairs: List[ConversationPair] = Field(default_factory=list)
    total_messages: int = Field(..., examples=[6])


class ConversationSummary(BaseModel):
    conversation_id: UUID = Field(..., examples=[uuid4()])
    first_question: str = Field(..., examples=["What is crop rotation?"])
    last_activity: str = Field(..., examples=["2024-03-22T10:30:00Z"])
    message_count: int = Field(..., examples=[4])


class UserConversations(BaseModel):
    user_id: str = Field(..., examples=["user123"])
    conversations: List[ConversationSummary] = Field(default_factory=list)


class ErrorResponse(BaseModel):
    detail: str = Field(..., examples=["AI service is temporarily unavailable."])


class IngestResponse(BaseModel):
    message: str = Field(..., examples=["Documents ingested successfully."])
    chunks_ingested: int = Field(..., examples=[12])
