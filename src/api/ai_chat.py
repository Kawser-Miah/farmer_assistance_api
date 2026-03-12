import io
from fastapi import APIRouter, HTTPException, UploadFile, File, status
from fastapi.concurrency import run_in_threadpool
from src.services.ai_chat.ai_chat_base import chat_with_ai
from src.services.ai_chat.rag.ingest import ingest_documents
from src.services.ai_chat.exceptions import (
    AIConfigurationError,
    EmbeddingServiceError,
    GeminiServiceError,
    VectorStoreError,
)
from src.core.config import settings
from src.schemas.ai_chat_schemas import ChatRequest, ChatResponse, ErrorResponse, IngestResponse

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
async def ai_chat(request: ChatRequest):
    try:
        response = await run_in_threadpool(chat_with_ai, request.query)
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