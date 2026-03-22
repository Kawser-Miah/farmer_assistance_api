from uuid import UUID
from typing import Optional
from src.services.ai_chat.rag.embeddings import generate_embedding
from src.services.ai_chat.rag.vector_store import search_documents
from src.services.ai_chat.rag.gemini_client import ask_gemini
from src.services.ai_chat.conversation_history import ConversationHistory


def chat_with_ai(query: str, user_id: str, conversation_id: Optional[UUID] = None, conversation_history: Optional[list] = None):
    """
    Chat with AI with optimized conversation history handling.

    Args:
        query: User's question
        user_id: Unique identifier for the user
        conversation_id: Optional conversation ID. If None, creates new conversation.
        conversation_history: Optional client-provided conversation history for efficiency

    Returns:
        Dict containing answer, sources, conversation_id, and updated conversation_history
    """
    cleaned_query = query.strip()
    if not cleaned_query:
        raise ValueError("Query cannot be empty.")

    # Create new conversation if not provided
    if conversation_id is None:
        conversation_id = ConversationHistory.create_new_conversation()

    # OPTIMIZATION: Use client-provided history or fetch from database
    if conversation_history:
        # Client provided history - use it directly (much faster!)
        conversation_context = ConversationHistory.format_conversation_for_client_history(conversation_history)
    else:
        # No client history - fetch from database (fallback)
        conversation_messages = ConversationHistory.get_conversation_history(conversation_id, limit=10)
        conversation_context = ConversationHistory.format_conversation_for_ai(conversation_messages)

    # 1 Embed question
    query_embedding = generate_embedding(cleaned_query)

    # 2 Search Supabase for relevant documents
    documents = search_documents(query_embedding)
    safe_documents = [doc for doc in documents if isinstance(doc, dict) and doc.get("content")]

    # 3 Create context from documents and conversation history
    document_context = "\n".join([doc["content"] for doc in safe_documents])
    if not document_context:
        document_context = "No specific documents found in knowledge base. Use your agricultural expertise to answer."

    # Combine conversation history and document context
    full_context = ""
    if conversation_context:
        full_context += f"Previous conversation:\n{conversation_context}\n\n"
    full_context += f"Knowledge base context:\n{document_context}"

    # 4 Ask Gemini with full context
    answer = ask_gemini(cleaned_query, full_context)

    # 5 Save the Q&A pair as a linked unit
    ConversationHistory.save_question_answer_pair(
        conversation_id=conversation_id,
        user_id=user_id,
        question=cleaned_query,
        answer=answer
    )

    # 6 Create updated conversation history for response
    from datetime import datetime, timezone
    current_time = datetime.now(timezone.utc).isoformat()

    # Build updated conversation history
    updated_conversation = []

    # Add existing conversation from client (if provided)
    if conversation_history:
        updated_conversation = conversation_history.copy()
    else:
        # Fallback: get from database and convert to proper format
        db_messages = ConversationHistory.get_conversation_history(conversation_id, limit=50)
        for msg in db_messages[:-2]:  # Exclude the new Q&A we just added
            updated_conversation.append({
                "role": msg["role"],
                "content": msg["content"],
                "timestamp": msg["created_at"]
            })

    # Add the new Q&A pair
    updated_conversation.extend([
        {
            "role": "user",
            "content": cleaned_query,
            "timestamp": current_time
        },
        {
            "role": "assistant",
            "content": answer,
            "timestamp": current_time
        }
    ])

    # Get the conversation title from database (generated only on first message)
    conversation_title = "Conversation"
    try:
        from src.core.database import supabase
        context_result = supabase.table("chat_context")\
            .select("title")\
            .eq("conversation_id", str(conversation_id))\
            .execute()

        if context_result.data:
            conversation_title = context_result.data[0].get("title", "Conversation")
    except Exception as e:
        print(f"Failed to get conversation title: {e}")

    return {
        "answer": answer,
        "sources": [{"content": doc["content"]} for doc in safe_documents],
        "conversation_id": conversation_id,
        "conversation_history": updated_conversation,
        "conversation_title": conversation_title
    }