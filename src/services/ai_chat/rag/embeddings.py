from sentence_transformers import SentenceTransformer
from src.services.ai_chat.exceptions import EmbeddingServiceError

_model = None


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        try:
            _model = SentenceTransformer("all-MiniLM-L6-v2")
        except Exception as exc:
            raise EmbeddingServiceError("Failed to initialize embedding model.") from exc
    return _model

def generate_embedding(text: str):
    try:
        model = _get_model()
        embedding = model.encode(text)
        return embedding.tolist()
    except EmbeddingServiceError:
        raise
    except Exception as exc:
        raise EmbeddingServiceError("Failed to generate embedding.") from exc