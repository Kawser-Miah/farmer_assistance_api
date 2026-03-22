"""
Conversation history management for AI chat.
Handles saving and retrieving chat messages from Supabase.
"""
from uuid import UUID, uuid4
from typing import List, Dict, Optional
from datetime import datetime, timezone
from src.core.database import supabase
from src.services.ai_chat.exceptions import VectorStoreError


class ConversationHistory:
    """Manages conversation history in Supabase."""

    @staticmethod
    def save_question_answer_pair(
        conversation_id: UUID,
        user_id: str,
        question: str,
        answer: str
    ) -> UUID:
        """
        Save a complete Q&A pair with proper linking using message_pair_id.

        Args:
            conversation_id: UUID of the conversation
            user_id: User identifier
            question: User's question
            answer: AI's answer

        Returns:
            UUID of the message pair
        """
        try:
            # Generate pair ID to link question and answer
            pair_id = uuid4()

            # Get next sequence numbers
            seq_result = supabase.table("chat_messages")\
                .select("sequence_number")\
                .eq("conversation_id", str(conversation_id))\
                .order("sequence_number", desc=True)\
                .limit(1)\
                .execute()

            next_seq = 1
            if seq_result.data:
                next_seq = seq_result.data[0]["sequence_number"] + 1

            # Insert question
            supabase.table("chat_messages").insert({
                "conversation_id": str(conversation_id),
                "user_id": user_id,
                "role": "user",
                "content": question,
                "message_pair_id": str(pair_id),
                "sequence_number": next_seq
            }).execute()

            # Insert answer
            supabase.table("chat_messages").insert({
                "conversation_id": str(conversation_id),
                "user_id": "system",  # AI responses
                "role": "assistant",
                "content": answer,
                "message_pair_id": str(pair_id),
                "sequence_number": next_seq + 1
            }).execute()

            # Update conversation context
            ConversationHistory._update_conversation_metadata(conversation_id, user_id)

            return pair_id

        except Exception as exc:
            raise VectorStoreError("Failed to save Q&A pair.") from exc

    @staticmethod
    def save_message(
        conversation_id: UUID,
        role: str,
        content: str,
        user_id: str = "unknown",
        message_pair_id: Optional[UUID] = None
    ) -> None:
        """
        Save a message to the chat_messages table.

        Args:
            conversation_id: UUID of the conversation
            role: Either 'user' or 'assistant'
            content: Message content
            user_id: User identifier
            message_pair_id: Optional pair ID for linking
        """
        try:
            # Get next sequence number
            seq_result = supabase.table("chat_messages")\
                .select("sequence_number")\
                .eq("conversation_id", str(conversation_id))\
                .order("sequence_number", desc=True)\
                .limit(1)\
                .execute()

            next_seq = 1
            if seq_result.data:
                next_seq = seq_result.data[0]["sequence_number"] + 1

            supabase.table("chat_messages").insert({
                "conversation_id": str(conversation_id),
                "user_id": user_id,
                "role": role,
                "content": content,
                "message_pair_id": str(message_pair_id) if message_pair_id else None,
                "sequence_number": next_seq
            }).execute()
        except Exception as exc:
            raise VectorStoreError(f"Failed to save message to conversation history.") from exc

    @staticmethod
    def get_conversation_history(
        conversation_id: UUID,
        limit: int = 10
    ) -> List[Dict]:
        """
        Retrieve conversation history ordered by sequence number.

        Args:
            conversation_id: UUID of the conversation
            limit: Maximum number of messages to retrieve

        Returns:
            List of message dictionaries with role and content
        """
        try:
            result = supabase.table("chat_messages")\
                .select("role, content, created_at, sequence_number")\
                .eq("conversation_id", str(conversation_id))\
                .order("sequence_number", desc=False)\
                .limit(limit)\
                .execute()

            return result.data or []
        except Exception as exc:
            raise VectorStoreError("Failed to retrieve conversation history.") from exc

    @staticmethod
    def create_new_conversation() -> UUID:
        """
        Create a new conversation ID.

        Returns:
            New UUID for the conversation
        """
        return uuid4()

    @staticmethod
    def update_conversation_context(
        conversation_id: UUID,
        summary: str
    ) -> None:
        """
        Update or insert conversation context/summary.

        Args:
            conversation_id: UUID of the conversation
            summary: Context summary for the conversation
        """
        try:
            # Use upsert to insert or update
            supabase.table("chat_context").upsert({
                "conversation_id": str(conversation_id),
                "summary": summary
            }).execute()
        except Exception as exc:
            raise VectorStoreError("Failed to update conversation context.") from exc

    @staticmethod
    def get_conversation_context(conversation_id: UUID) -> Optional[str]:
        """
        Get conversation context/summary.

        Args:
            conversation_id: UUID of the conversation

        Returns:
            Summary string or None if not found
        """
        try:
            result = supabase.table("chat_context")\
                .select("summary")\
                .eq("conversation_id", str(conversation_id))\
                .execute()

            if result.data:
                return result.data[0]["summary"]
            return None
        except Exception as exc:
            raise VectorStoreError("Failed to retrieve conversation context.") from exc

    @staticmethod
    def format_conversation_for_ai(messages: List[Dict]) -> str:
        """
        Format conversation history for AI context with proper Q&A pairing.

        Args:
            messages: List of message dictionaries

        Returns:
            Formatted conversation string with paired questions and answers
        """
        if not messages:
            return ""

        formatted_pairs = []
        current_user_msg = None

        for msg in messages:
            if msg["role"] == "user":
                current_user_msg = msg["content"]
            elif msg["role"] == "assistant" and current_user_msg:
                # Pair user question with assistant answer
                formatted_pairs.append(f"User: {current_user_msg}")
                formatted_pairs.append(f"Assistant: {msg['content']}")
                current_user_msg = None  # Reset after pairing

        # Handle case where last message is a user message without an answer
        if current_user_msg:
            formatted_pairs.append(f"User: {current_user_msg}")

        return "\n".join(formatted_pairs)

    @staticmethod
    def format_conversation_for_client_history(client_history: List[Dict]) -> str:
        """
        Format client-provided conversation history for AI context.

        Args:
            client_history: List of client message dictionaries with role, content, timestamp

        Returns:
            Formatted conversation string with Q&A pairing
        """
        if not client_history:
            return ""

        formatted_pairs = []
        current_user_msg = None

        for msg in client_history:
            if msg["role"] == "user":
                current_user_msg = msg["content"]
            elif msg["role"] == "assistant" and current_user_msg:
                # Pair user question with assistant answer
                formatted_pairs.append(f"User: {current_user_msg}")
                formatted_pairs.append(f"Assistant: {msg['content']}")
                current_user_msg = None  # Reset after pairing

        # Handle case where last message is a user message without an answer
        if current_user_msg:
            formatted_pairs.append(f"User: {current_user_msg}")

        return "\n".join(formatted_pairs)

    @staticmethod
    def get_conversation_pairs(
        conversation_id: UUID,
        limit: int = 5
    ) -> List[Dict]:
        """
        Retrieve conversation history as properly linked question-answer pairs using message_pair_id.

        Args:
            conversation_id: UUID of the conversation
            limit: Maximum number of Q&A pairs to retrieve

        Returns:
            List of Q&A pair dictionaries: [{"question": str, "answer": str, "timestamp": str}]
        """
        try:
            # Get all messages for the conversation
            result = supabase.table("chat_messages")\
                .select("role, content, created_at, message_pair_id, sequence_number")\
                .eq("conversation_id", str(conversation_id))\
                .order("sequence_number", desc=False)\
                .execute()

            messages = result.data or []

            # Group by message_pair_id for proper linking
            pairs_dict = {}
            unpaired_questions = []

            for msg in messages:
                if msg["message_pair_id"]:
                    # Has pair ID - group by it
                    pair_id = msg["message_pair_id"]
                    if pair_id not in pairs_dict:
                        pairs_dict[pair_id] = {"question": None, "answer": None, "timestamp": None}

                    if msg["role"] == "user":
                        pairs_dict[pair_id]["question"] = msg["content"]
                        pairs_dict[pair_id]["timestamp"] = msg["created_at"]
                    elif msg["role"] == "assistant":
                        pairs_dict[pair_id]["answer"] = msg["content"]
                else:
                    # No pair ID - handle as unpaired (fallback for old data)
                    if msg["role"] == "user":
                        unpaired_questions.append({
                            "question": msg["content"],
                            "answer": None,
                            "timestamp": msg["created_at"]
                        })

            # Convert to list and add unpaired questions
            pairs = []
            for pair_data in pairs_dict.values():
                if pair_data["question"]:  # Only include if we have a question
                    pairs.append(pair_data)

            # Add unpaired questions at the end
            pairs.extend(unpaired_questions)

            # Limit results
            return pairs[:limit]

        except Exception as exc:
            raise VectorStoreError("Failed to retrieve conversation pairs.") from exc

    @staticmethod
    def get_user_conversations(user_id: str, limit: int = 20) -> List[Dict]:
        """
        Get all conversations for a specific user using the updated schema.

        Args:
            user_id: User identifier
            limit: Maximum number of conversations to retrieve

        Returns:
            List of conversation summaries with metadata
        """
        try:
            # Get conversation summary from context table
            context_result = supabase.table("chat_context")\
                .select("conversation_id, title, summary, total_messages, last_activity")\
                .eq("user_id", user_id)\
                .order("last_activity", desc=True)\
                .limit(limit)\
                .execute()

            conversations = []
            if context_result.data:
                # Use context data if available
                for ctx in context_result.data:
                    # Get first question
                    first_msg = supabase.table("chat_messages")\
                        .select("content")\
                        .eq("conversation_id", ctx["conversation_id"])\
                        .eq("role", "user")\
                        .order("sequence_number", desc=False)\
                        .limit(1)\
                        .execute()

                    first_question = "Untitled conversation"
                    if first_msg.data:
                        first_question = first_msg.data[0]["content"][:50] + "..."

                    conversations.append({
                        "conversation_id": ctx["conversation_id"],
                        "title": ctx.get("title") or first_question,
                        "first_question": first_question,
                        "last_activity": ctx["last_activity"],
                        "message_count": ctx.get("total_messages", 0)
                    })
            else:
                # Fallback: get conversations by finding unique conversation_ids by user_id
                all_messages = supabase.table("chat_messages")\
                    .select("conversation_id, content, role, created_at")\
                    .eq("user_id", user_id)\
                    .order("created_at", desc=True)\
                    .limit(1000)\
                    .execute()

                conversations_dict = {}
                for msg in all_messages.data or []:
                    conv_id = msg["conversation_id"]
                    if conv_id not in conversations_dict:
                        conversations_dict[conv_id] = {
                            "conversation_id": conv_id,
                            "first_question": None,
                            "last_activity": msg["created_at"],
                            "message_count": 0
                        }

                    conversations_dict[conv_id]["message_count"] += 1

                    # Set first question (earliest user message)
                    if msg["role"] == "user" and not conversations_dict[conv_id]["first_question"]:
                        conversations_dict[conv_id]["first_question"] = msg["content"]

                conversations = list(conversations_dict.values())[:limit]

            return conversations

        except Exception as exc:
            raise VectorStoreError("Failed to get user conversations.") from exc

    @staticmethod
    def _update_conversation_metadata(conversation_id: UUID, user_id: str):
        """
        Update conversation context metadata.

        Args:
            conversation_id: UUID of the conversation
            user_id: User identifier
        """
        try:
            # Count total messages for this conversation
            msg_count_result = supabase.table("chat_messages")\
                .select("id")\
                .eq("conversation_id", str(conversation_id))\
                .execute()

            total_messages = len(msg_count_result.data) if msg_count_result.data else 0

            # Check if conversation context already exists
            existing_context = supabase.table("chat_context")\
                .select("conversation_id, title")\
                .eq("conversation_id", str(conversation_id))\
                .execute()

            # Only generate title if this is a NEW conversation
            title = "New Conversation"  # Default fallback
            if existing_context.data:
                # Use existing title - don't regenerate
                title = existing_context.data[0].get("title", "Conversation")
            else:
                # This is a new conversation - generate AI title from first question
                first_msg_result = supabase.table("chat_messages")\
                    .select("content")\
                    .eq("conversation_id", str(conversation_id))\
                    .eq("role", "user")\
                    .order("sequence_number", desc=False)\
                    .limit(1)\
                    .execute()

                if first_msg_result.data:
                    first_question = first_msg_result.data[0]["content"]
                    # Use AI to generate title ONLY for the first time
                    title = ConversationHistory.generate_conversation_title(first_question)

            # Create or update context record
            current_time = datetime.now(timezone.utc).isoformat()
            context_data = {
                "conversation_id": str(conversation_id),
                "user_id": user_id,
                "title": title,
                "summary": None,  # Set summary as null for now
                "total_messages": total_messages,
                "last_activity": current_time
            }

            # Try upsert first, if it fails, do insert/update manually
            try:
                if existing_context.data:
                    # Update existing record - preserve the title, only update counts and timestamp
                    supabase.table("chat_context")\
                        .update({
                            "total_messages": total_messages,
                            "last_activity": current_time
                        })\
                        .eq("conversation_id", str(conversation_id))\
                        .execute()
                else:
                    # Insert new record with AI-generated title
                    supabase.table("chat_context").insert(context_data).execute()
            except Exception:
                # Fallback: check if record exists and update/insert accordingly
                fallback_existing = supabase.table("chat_context")\
                    .select("conversation_id")\
                    .eq("conversation_id", str(conversation_id))\
                    .execute()

                if fallback_existing.data:
                    # Update existing record - preserve title
                    supabase.table("chat_context")\
                        .update({
                            "total_messages": total_messages,
                            "last_activity": current_time
                        })\
                        .eq("conversation_id", str(conversation_id))\
                        .execute()
                else:
                    # Insert new record with generated title
                    supabase.table("chat_context").insert(context_data).execute()

        except Exception as exc:
            # Log error but don't fail the main operation
            print(f"Warning: Failed to update conversation metadata: {exc}")
            pass

    @staticmethod
    def ensure_conversation_context(conversation_id: UUID, user_id: str) -> bool:
        """
        Manually ensure a conversation context record exists.

        Args:
            conversation_id: UUID of the conversation
            user_id: User identifier

        Returns:
            True if context was created/updated successfully
        """
        try:
            ConversationHistory._update_conversation_metadata(conversation_id, user_id)
            return True
        except Exception as exc:
            print(f"Failed to ensure conversation context: {exc}")
            return False

    @staticmethod
    def delete_conversation(conversation_id: UUID) -> bool:
        """
        Delete a conversation and all its messages.

        Args:
            conversation_id: UUID of the conversation to delete

        Returns:
            True if successful
        """
        try:
            # Delete messages
            supabase.table("chat_messages")\
                .delete()\
                .eq("conversation_id", str(conversation_id))\
                .execute()

            # Delete context if exists
            supabase.table("chat_context")\
                .delete()\
                .eq("conversation_id", str(conversation_id))\
                .execute()

            return True
        except Exception as exc:
            raise VectorStoreError("Failed to delete conversation.") from exc

    @staticmethod
    def generate_conversation_title(first_question: str) -> str:
        """
        Generate an AI-powered title based on the first question.

        Args:
            first_question: The user's first question in the conversation

        Returns:
            Generated title (max 100 characters)
        """
        try:
            # Import here to avoid circular imports
            from src.services.ai_chat.rag.gemini_client import ask_gemini

            title_prompt = f"""
Based on this user question about farming/agriculture, generate a concise, descriptive title for this conversation.

User Question: "{first_question}"

Generate a title that:
- Is 3-8 words maximum
- Describes the main topic clearly
- Is helpful for organizing conversations
- Uses farming/agricultural terminology when relevant
- No quotes or special formatting

Examples:
- "Tomato Fertilizer Recommendations"
- "Pest Control for Cucumber Plants"
- "Organic Farming Techniques"
- "Soil pH Management"

Title:"""

            generated_title = ask_gemini(title_prompt, "")

            # Clean and validate the title
            title = generated_title.strip()

            # Remove quotes if present
            if title.startswith('"') and title.endswith('"'):
                title = title[1:-1]
            if title.startswith("'") and title.endswith("'"):
                title = title[1:-1]

            # Ensure it's not too long
            if len(title) > 100:
                title = title[:97] + "..."

            # Fallback if generation failed
            if not title or len(title) < 3:
                # Use first few words of the question
                words = first_question.split()[:6]
                title = " ".join(words)
                if len(title) > 50:
                    title = title[:47] + "..."

            return title

        except Exception as exc:
            # Fallback to simple truncation if AI generation fails
            print(f"Title generation failed, using fallback: {exc}")
            words = first_question.split()[:6]
            title = " ".join(words)
            if len(title) > 50:
                title = title[:47] + "..."
            return title