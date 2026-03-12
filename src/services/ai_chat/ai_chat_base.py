from src.services.ai_chat.rag.embeddings import generate_embedding
from src.services.ai_chat.rag.vector_store import search_documents
from src.services.ai_chat.rag.gemini_client import ask_gemini


def chat_with_ai(query: str):

    # 1 Embed question
    query_embedding = generate_embedding(query)

    # 2 Search Supabase
    documents = search_documents(query_embedding)

    # 3 Create context
    context = "\n".join([doc["content"] for doc in documents])

    # 4 Ask Gemini
    answer = ask_gemini(query, context)

    return {
        "answer": answer,
        "sources": documents
    }