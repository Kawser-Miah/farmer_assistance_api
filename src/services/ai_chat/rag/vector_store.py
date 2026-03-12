from supabase import create_client
from src.core.config import settings
from dotenv import load_dotenv
from src.core.database import supabase

def insert_document(content: str, embedding: list):

    supabase.table("documents").insert({
        "content": content,
        "embedding": embedding
    }).execute()
    
def search_documents(query_embedding):

    result = supabase.rpc(
        "match_documents",
        {
            "query_embedding": query_embedding,
            "match_count": 5
        }
    ).execute()

    return result.data