"""
Example usage of the improved conversation history system.
This demonstrates proper question-answer pairing and tracking.
"""
import json
from uuid import UUID
from src.services.ai_chat.conversation_history import ConversationHistory

def test_conversation_pairing():
    """Test the conversation history Q&A pairing functionality."""

    print("=== Testing Conversation History Q&A Pairing ===")

    # Create a test conversation
    conversation_id = ConversationHistory.create_new_conversation()
    print(f"Created conversation: {conversation_id}")

    # Simulate a conversation flow
    print("\n1. Saving messages in order:")

    # Question 1
    ConversationHistory.save_message(conversation_id, "user", "What is crop rotation?")
    print("   Saved: User asks about crop rotation")

    # Answer 1
    ConversationHistory.save_message(conversation_id, "assistant", "Crop rotation is the practice of growing different crops in the same area across seasons.")
    print("   Saved: Assistant explains crop rotation")

    # Question 2
    ConversationHistory.save_message(conversation_id, "user", "How often should I rotate?")
    print("   Saved: User asks about frequency")

    # Answer 2
    ConversationHistory.save_message(conversation_id, "assistant", "Most farmers rotate crops annually or every 2-3 years depending on the crop type.")
    print("   Saved: Assistant explains rotation frequency")

    print("\n2. Retrieving conversation history:")

    # Get regular conversation history
    messages = ConversationHistory.get_conversation_history(conversation_id, limit=10)
    print(f"   Retrieved {len(messages)} messages")

    # Get formatted conversation for AI
    formatted = ConversationHistory.format_conversation_for_ai(messages)
    print("\n   Formatted for AI context:")
    print(f"   {formatted}")

    # Get Q&A pairs
    pairs = ConversationHistory.get_conversation_pairs(conversation_id, limit=5)
    print(f"\n3. Retrieved {len(pairs)} Q&A pairs:")

    for i, pair in enumerate(pairs, 1):
        print(f"\n   Pair {i}:")
        print(f"   Q: {pair['question']}")
        print(f"   A: {pair['answer']}")
        print(f"   Time: {pair['timestamp']}")

def test_api_usage():
    """Show API usage examples with the new conversation tracking."""
    print("\n\n=== API Usage Examples ===")

    # Example 1: New conversation
    print("1. Start new conversation:")
    request1 = {
        "query": "What is the best fertilizer for tomatoes?",
        "user_id": "farmer123"
        # No conversation_id = new conversation
    }
    print(f"   POST /ai-chat/chat")
    print(f"   Body: {json.dumps(request1, indent=4)}")
    print(f"   Response will include: conversation_id for tracking")

    # Example 2: Continue conversation
    print("\n2. Continue conversation:")
    request2 = {
        "query": "How much fertilizer should I apply?",
        "user_id": "farmer123",
        "conversation_id": "550e8400-e29b-41d4-a716-446655440000"
    }
    print(f"   POST /ai-chat/chat")
    print(f"   Body: {json.dumps(request2, indent=4)}")
    print(f"   AI will remember previous question about tomato fertilizer")

def test_user_level_apis():
    """Show user-level API examples for conversation management."""
    print("\n\n=== USER-LEVEL API EXAMPLES ===")

    base_url = "http://localhost:8000/ai-chat"

    print("1. 💬 CHAT WITH AI:")
    print("   POST /ai-chat/chat")
    print("   Body:")
    chat_request = {
        "query": "What is the best fertilizer for tomatoes?",
        "user_id": "farmer123"
    }
    print(f"   {json.dumps(chat_request, indent=4)}")
    print("   Response: AI answer + conversation_id")

    print("\n2. 📋 GET USER'S ALL CONVERSATIONS:")
    print("   GET /ai-chat/conversations/farmer123?limit=10")
    print("   Response:")
    user_conversations_example = {
        "user_id": "farmer123",
        "conversations": [
            {
                "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
                "first_question": "What is the best fertilizer for tomatoes?",
                "last_activity": "2024-03-22T15:30:00Z",
                "message_count": 6
            },
            {
                "conversation_id": "660f9511-f30c-52e5-b827-557766551111",
                "first_question": "How do I treat plant diseases?",
                "last_activity": "2024-03-21T10:15:00Z",
                "message_count": 4
            }
        ]
    }
    print(f"   {json.dumps(user_conversations_example, indent=4)}")

    print("\n3. 🔍 GET SPECIFIC CONVERSATION HISTORY:")
    print("   GET /ai-chat/conversations/farmer123/550e8400-e29b-41d4-a716-446655440000")
    print("   Response:")
    conversation_history_example = {
        "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
        "total_messages": 6,
        "pairs": [
            {
                "question": "What is the best fertilizer for tomatoes?",
                "answer": "For tomatoes, I recommend using a balanced fertilizer like 10-10-10...",
                "timestamp": "2024-03-22T15:25:00Z"
            },
            {
                "question": "How much should I apply?",
                "answer": "Apply 2-3 tablespoons per plant every 2-3 weeks...",
                "timestamp": "2024-03-22T15:28:00Z"
            },
            {
                "question": "When is the best time to fertilize?",
                "answer": "The best time is early morning or late evening...",
                "timestamp": "2024-03-22T15:30:00Z"
            }
        ]
    }
    print(f"   {json.dumps(conversation_history_example, indent=4)}")

    print("\n4. 🗑️ DELETE CONVERSATION:")
    print("   DELETE /ai-chat/conversations/farmer123/550e8400-e29b-41d4-a716-446655440000")
    print("   Response: {'message': 'Conversation deleted successfully'}")

def test_mobile_app_workflow():
    """Example mobile app workflow using the conversation APIs."""
    print("\n\n=== 📱 MOBILE APP WORKFLOW EXAMPLE ===")

    print("SCENARIO: User opens the chat app")

    print("\nStep 1: Load user's conversation list")
    print("   API Call: GET /ai-chat/conversations/farmer123")
    print("   App shows: List of previous conversations")

    print("\nStep 2: User taps on a conversation")
    print("   API Call: GET /ai-chat/conversations/farmer123/{conversation_id}")
    print("   App shows: Full Q&A history for that conversation")

    print("\nStep 3: User asks a new question in existing conversation")
    print("   API Call: POST /ai-chat/chat")
    print("   Body: { query: 'new question', user_id: 'farmer123', conversation_id: 'existing_id' }")
    print("   App shows: AI response + updates conversation")

    print("\nStep 4: User starts a completely new conversation")
    print("   API Call: POST /ai-chat/chat")
    print("   Body: { query: 'new question', user_id: 'farmer123' }  // No conversation_id")
    print("   App shows: AI response + creates new conversation")

    print("\nStep 5: User wants to delete old conversation")
    print("   API Call: DELETE /ai-chat/conversations/farmer123/{conversation_id}")
    print("   App shows: Conversation removed from list")

    print("\n✅ BENEFITS FOR USERS:")
    print("   • See all their past conversations")
    print("   • Continue old conversations with context")
    print("   • Start fresh conversations anytime")
    print("   • Delete conversations they no longer need")
    print("   • Questions and answers are properly paired")

if __name__ == "__main__":
    test_conversation_pairing()
    test_api_usage()
    test_user_level_apis()
    test_mobile_app_workflow()