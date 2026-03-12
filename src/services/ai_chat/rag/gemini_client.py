from google import genai
from src.core.config import settings
from src.services.ai_chat.exceptions import AIConfigurationError, GeminiServiceError

_client = None


def _get_client() -> genai.Client:
    global _client
    if _client is not None:
        return _client

    api_key = settings.google_api_key.strip()
    if not api_key:
        raise AIConfigurationError("GOOGLE_API_KEY is missing. Set it in your .env file.")

    try:
        _client = genai.Client(api_key=api_key)
        return _client
    except Exception as exc:
        raise GeminiServiceError("Failed to initialize Gemini client.") from exc


def ask_gemini(question: str, context: str):

    prompt = f"""
    You are an agriculture expert assistant.

    Use the context to answer the farmer's question.

    Context:
    {context}

    Question:
    {question}
    """

    try:
        client = _get_client()
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        text = response.text
        if not text:
            raise GeminiServiceError("Gemini returned an empty response.")
        return text
    except (AIConfigurationError, GeminiServiceError):
        raise
    except Exception as exc:
        raise GeminiServiceError("Failed to generate response from Gemini.") from exc