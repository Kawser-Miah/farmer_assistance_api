from src.core.database import supabase
from src.services.ai_chat.exceptions import VectorStoreError

def insert_document(content: str, embedding: list):
    try:
        supabase.table("documents").insert({
            "content": content,
            "embedding": embedding
        }).execute()
    except Exception as exc:
        raise VectorStoreError("Failed to insert document into vector store.") from exc
    
def search_documents(query_embedding):
    try:
        result = supabase.rpc(
            "match_documents",
            {
                "query_embedding": query_embedding,
                "match_count": 5
            }
        ).execute()
        return result.data or []
    except Exception as exc:
        raise VectorStoreError("Failed to search documents from vector store.") from exc