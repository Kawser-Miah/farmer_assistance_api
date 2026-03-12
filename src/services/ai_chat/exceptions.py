class AIChatError(Exception):
    """Base exception for AI chat errors."""


class EmbeddingServiceError(AIChatError):
    """Raised when embedding generation fails."""


class VectorStoreError(AIChatError):
    """Raised when vector store operations fail."""


class GeminiServiceError(AIChatError):
    """Raised when Gemini request fails."""


class AIConfigurationError(AIChatError):
    """Raised when required AI configuration is missing or invalid."""
