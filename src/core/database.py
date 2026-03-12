from supabase import create_client
from src.core.config import settings

supabase = create_client(
    settings.supabase_url,
    settings.supabase_anon_key
)
