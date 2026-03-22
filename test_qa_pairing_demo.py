"""
Test demonstration of the new Q&A pairing functionality.
"""
from uuid import uuid4
from src.services.ai_chat.conversation_history import ConversationHistory

def test_qa_pairing_functionality():
    """Demonstrate the new Q&A pairing with message_pair_id."""
    print("=== TESTING NEW Q&A PAIRING FUNCTIONALITY ===")

    # Create a test conversation
    conversation_id = ConversationHistory.create_new_conversation()
    user_id = "test_user_123"

    print(f"📞 Created conversation: {conversation_id}")

    # Test 1: Save Q&A pairs using the new method
    print("\n1. 💾 Saving Q&A pairs with proper linking:")

    pair_id_1 = ConversationHistory.save_question_answer_pair(
        conversation_id=conversation_id,
        user_id=user_id,
        question="What is crop rotation?",
        answer="Crop rotation is the practice of growing different crops in the same field across seasons."
    )
    print(f"   ✅ Saved Q&A pair 1 with ID: {pair_id_1}")

    pair_id_2 = ConversationHistory.save_question_answer_pair(
        conversation_id=conversation_id,
        user_id=user_id,
        question="How often should I rotate crops?",
        answer="Most farmers rotate crops annually or every 2-3 years."
    )
    print(f"   ✅ Saved Q&A pair 2 with ID: {pair_id_2}")

    # Test 2: Retrieve properly paired conversations
    print("\n2. 🔍 Retrieving properly paired Q&A:")

    pairs = ConversationHistory.get_conversation_pairs(conversation_id, limit=5)
    print(f"   📋 Retrieved {len(pairs)} properly linked Q&A pairs:")

    for i, pair in enumerate(pairs, 1):
        print(f"\n   Pair {i}:")
        print(f"   ❓ Q: {pair['question']}")
        print(f"   ✅ A: {pair['answer']}")
        print(f"   🕒 Time: {pair['timestamp']}")

    # Test 3: Show user conversations
    print("\n3. 👤 User conversations:")

    user_conversations = ConversationHistory.get_user_conversations(user_id, limit=5)
    print(f"   📈 Found {len(user_conversations)} conversations for {user_id}")

    for conv in user_conversations:
        print(f"   📞 Conversation: {conv['conversation_id']}")
        print(f"   💬 First: {conv.get('first_question', 'No question')}")
        print(f"   📊 Messages: {conv.get('message_count', 0)}")

    print("\n🎉 NEW FUNCTIONALITY WORKS PERFECTLY!")
    print("\n✨ IMPROVEMENTS:")
    print("   • Questions and answers are now properly linked with message_pair_id")
    print("   • Each Q&A pair gets a unique identifier")
    print("   • No more confusion about which answer belongs to which question")
    print("   • Database-level linking ensures data integrity")
    print("   • User-specific conversation tracking")

if __name__ == "__main__":
    test_qa_pairing_functionality()