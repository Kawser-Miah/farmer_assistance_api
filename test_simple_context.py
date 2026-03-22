"""
Simple test to verify chat_context table is working after schema fix.
"""
from uuid import uuid4
from src.services.ai_chat.conversation_history import ConversationHistory

def test_simple_chat_context():
    """Simple test for chat_context functionality."""
    print("=== TESTING CHAT CONTEXT AFTER SCHEMA FIX ===")

    try:
        # Create a simple test
        conversation_id = ConversationHistory.create_new_conversation()
        user_id = "test_user_simple"

        print(f"📞 Test conversation: {conversation_id}")
        print(f"👤 Test user: {user_id}")

        # Try to save a simple Q&A pair
        print("\n1. 💾 Saving Q&A pair...")

        pair_id = ConversationHistory.save_question_answer_pair(
            conversation_id=conversation_id,
            user_id=user_id,
            question="Test question?",
            answer="Test answer."
        )

        print(f"   ✅ Success! Pair ID: {pair_id}")
        print("   🎉 Chat context table is now working!")

    except Exception as exc:
        print(f"   ❌ Error: {exc}")
        print("\n🔧 TROUBLESHOOTING:")
        print("   1. Make sure you ran the schema fix commands in Supabase")
        print("   2. Check that 'summary' column is now nullable")
        print("   3. Verify 'user_id' column exists")

        if "summary" in str(exc):
            print("\n💡 LIKELY ISSUE: Summary column is still NOT NULL")
            print("   Run this in Supabase SQL editor:")
            print("   ALTER TABLE chat_context ALTER COLUMN summary DROP NOT NULL;")

        if "user_id" in str(exc):
            print("\n💡 LIKELY ISSUE: user_id column missing")
            print("   Run this in Supabase SQL editor:")
            print("   ALTER TABLE chat_context ADD COLUMN user_id TEXT DEFAULT 'unknown';")

if __name__ == "__main__":
    test_simple_chat_context()