from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000, examples=["How can I treat powdery mildew in cucumber?"])


class ChatSource(BaseModel):
    content: str = Field(..., examples=["Powdery mildew appears as white powder on leaves."])


class ChatResponse(BaseModel):
    answer: str = Field(..., examples=["Use sulfur-based fungicide and improve airflow around plants."])
    sources: list[ChatSource] = Field(default_factory=list)


class ErrorResponse(BaseModel):
    detail: str = Field(..., examples=["AI service is temporarily unavailable."])


class IngestResponse(BaseModel):
    message: str = Field(..., examples=["Documents ingested successfully."])
    chunks_ingested: int = Field(..., examples=[12])
