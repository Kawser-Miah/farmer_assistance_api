import io
from fastapi import APIRouter, HTTPException, UploadFile, File, status, Path, Query, Depends
from fastapi.concurrency import run_in_threadpool
from uuid import UUID
from src.core.jwt_validation import decode_supabase_jwt
from src.services.ai_chat.ai_chat_base import chat_with_ai
from src.services.ai_chat.rag.ingest import ingest_documents
from src.services.ai_chat.conversation_history import ConversationHistory
from src.services.ai_chat.exceptions import (
    AIConfigurationError,
    EmbeddingServiceError,
    GeminiServiceError,
    VectorStoreError,
)
from src.core.config import settings
from src.schemas.ai_chat_schemas import (
    ChatRequest,
    ChatResponse,
    ErrorResponse,
    IngestResponse,
    ConversationHistory as ConversationHistorySchema,
    UserConversations,
    ConversationPair,
    ChatMessage
)

_MAX_UPLOAD_BYTES = 10 * 1024 * 1024  # 10 MB


router = APIRouter(
    prefix=settings.ai_chat_prefix,
    tags=["AI Chat"]
)


@router.post(
    "/chat",
    response_model=ChatResponse,
    responses={
        400: {"model": ErrorResponse},
        503: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def ai_chat(request: ChatRequest, user_id: str = Depends(decode_supabase_jwt)):
    try:
        # Convert ChatMessage objects to dict format for processing
        client_history = None
        if request.conversation_history:
            client_history = [
                {
                    "role": msg.role,
                    "content": msg.content,
                    "timestamp": msg.timestamp
                }
                for msg in request.conversation_history
            ]

        response = await run_in_threadpool(
            chat_with_ai,
            request.query,
            user_id,
            request.conversation_id,
            client_history
        )
        return response
    except AIConfigurationError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
    except (EmbeddingServiceError, VectorStoreError, GeminiServiceError) as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while processing chat request.",
        ) from exc


@router.get(
    "/conversations/{user_id}",
    response_model=UserConversations,
    summary="Get all conversations for a user",
    description="Retrieve all conversation summaries for a specific user",
    responses={
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def get_user_conversations(
    user_id: str = Path(..., description="User ID to get conversations for"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of conversations to return")
):
    try:
        conversations_data = await run_in_threadpool(
            ConversationHistory.get_user_conversations,
            user_id,
            limit
        )

        return UserConversations(
            user_id=user_id,
            conversations=conversations_data
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user conversations.",
        ) from exc


@router.get(
    "/conversations/{user_id}/{conversation_id}",
    response_model=ConversationHistorySchema,
    summary="Get conversation history",
    description="Retrieve Q&A pairs from a specific conversation",
    responses={
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def get_conversation_history(
    user_id: str = Path(..., description="User ID"),
    conversation_id: UUID = Path(..., description="Conversation ID"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of Q&A pairs to return")
):
    try:
        # Get Q&A pairs
        pairs_data = await run_in_threadpool(
            ConversationHistory.get_conversation_pairs,
            conversation_id,
            limit
        )

        # Get total message count
        messages = await run_in_threadpool(
            ConversationHistory.get_conversation_history,
            conversation_id,
            1000  # Get all to count
        )

        conversation_pairs = [
            ConversationPair(
                question=pair["question"],
                answer=pair["answer"],
                timestamp=pair["timestamp"]
            )
            for pair in pairs_data
        ]

        return ConversationHistorySchema(
            conversation_id=conversation_id,
            pairs=conversation_pairs,
            total_messages=len(messages)
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve conversation history.",
        ) from exc


@router.delete(
    "/conversations/{user_id}/{conversation_id}",
    summary="Delete a conversation",
    description="Delete a conversation and all its messages",
    responses={
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def delete_conversation(
    user_id: str = Path(..., description="User ID"),
    conversation_id: UUID = Path(..., description="Conversation ID to delete")
):
    try:
        success = await run_in_threadpool(
            ConversationHistory.delete_conversation,
            conversation_id
        )

        if success:
            return {"message": "Conversation deleted successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found",
            )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete conversation.",
        ) from exc


def _extract_text(file: UploadFile, raw: bytes) -> str:
    """Extract plain text from a .txt or .pdf upload."""
    if file.filename.endswith(".pdf"):
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(raw))
        return "\n\n".join(page.extract_text() or "" for page in reader.pages)
    return raw.decode("utf-8", errors="replace")


def _chunk_text(text: str, max_chars: int = 1000) -> list[str]:
    """Split text into non-empty chunks by paragraph, capped at max_chars."""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: list[str] = []
    current = ""
    for para in paragraphs:
        if len(current) + len(para) + 2 > max_chars and current:
            chunks.append(current.strip())
            current = para
        else:
            current = (current + "\n\n" + para) if current else para
    if current:
        chunks.append(current.strip())
    return chunks


@router.post(
    "/ingest",
    response_model=IngestResponse,
    summary="Ingest a document into the knowledge base",
    description="Upload a .txt or .pdf file. The text is split into chunks and stored in the vector DB for RAG.",
    responses={
        400: {"model": ErrorResponse},
        503: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def ingest_document(
    file: UploadFile = File(..., description="A .txt or .pdf file to ingest."),
):
    if not (file.filename.endswith(".txt") or file.filename.endswith(".pdf")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only .txt and .pdf files are supported.",
        )

    raw = await file.read()
    if len(raw) > _MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File exceeds the 10 MB size limit.",
        )
    if not raw:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty.",
        )

    try:
        text = await run_in_threadpool(_extract_text, file, raw)
        chunks = _chunk_text(text)
        if not chunks:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No text content found in the uploaded file.",
            )
        await run_in_threadpool(ingest_documents, chunks)
        return IngestResponse(message="Documents ingested successfully.", chunks_ingested=len(chunks))
    except HTTPException:
        raise
    except (EmbeddingServiceError, VectorStoreError, AIConfigurationError) as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during ingestion.",
        ) from exc