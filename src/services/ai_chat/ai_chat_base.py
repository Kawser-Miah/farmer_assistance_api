from src.services.ai_chat.rag.embeddings import generate_embedding
from src.services.ai_chat.rag.vector_store import search_documents
from src.services.ai_chat.rag.gemini_client import ask_gemini


def chat_with_ai(query: str):
    cleaned_query = query.strip()
    if not cleaned_query:
        raise ValueError("Query cannot be empty.")

    # 1 Embed question
    query_embedding = generate_embedding(cleaned_query)

    # 2 Search Supabase
    documents = search_documents(query_embedding)
    safe_documents = [doc for doc in documents if isinstance(doc, dict) and doc.get("content")]

    # 3 Create context
    context = "\n".join([doc["content"] for doc in safe_documents])
    if not context:
        context = "No specific documents found in knowledge base. Use your agricultural expertise to answer."

    # 4 Ask Gemini
    answer = ask_gemini(cleaned_query, context)

    return {
        "answer": answer,
        "sources": [{"content": doc["content"]} for doc in safe_documents]
    }