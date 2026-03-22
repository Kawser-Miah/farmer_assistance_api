"""
Test script to verify chat_context table is being updated correctly.
"""
from uuid import uuid4
from src.services.ai_chat.conversation_history import ConversationHistory
from src.core.database import supabase

def test_chat_context_updates():
    """Test the chat_context table updates."""
    print("=== TESTING CHAT CONTEXT TABLE UPDATES ===")

    # Create test data
    conversation_id = ConversationHistory.create_new_conversation()
    user_id = "test_user_context"

    print(f"📞 Created test conversation: {conversation_id}")
    print(f"👤 User ID: {user_id}")

    # Test 1: Save a Q&A pair and check if context is updated
    print("\n1. 💾 Saving Q&A pair and checking context update:")

    pair_id = ConversationHistory.save_question_answer_pair(
        conversation_id=conversation_id,
        user_id=user_id,
        question="What is the best fertilizer for tomatoes?",
        answer="For tomatoes, I recommend using a balanced fertilizer with NPK ratio 10-10-10."
    )

    print(f"   ✅ Saved Q&A pair: {pair_id}")

    # Check if context was created
    print("\n2. 🔍 Checking chat_context table:")

    try:
        context_result = supabase.table("chat_context")\
            .select("*")\
            .eq("conversation_id", str(conversation_id))\
            .execute()

        if context_result.data:
            context = context_result.data[0]
            print("   ✅ Context record found:")
            print(f"      🆔 Conversation ID: {context['conversation_id']}")
            print(f"      👤 User ID: {context['user_id']}")
            print(f"      📝 Title: {context.get('title', 'None')}")
            print(f"      📊 Total Messages: {context.get('total_messages', 0)}")
            print(f"      🕒 Last Activity: {context.get('last_activity', 'None')}")
        else:
            print("   ❌ No context record found!")
            print("   🔧 Trying to manually create context...")

            # Try manual context creation
            success = ConversationHistory.ensure_conversation_context(conversation_id, user_id)
            if success:
                print("   ✅ Manual context creation successful!")

                # Check again
                context_result = supabase.table("chat_context")\
                    .select("*")\
                    .eq("conversation_id", str(conversation_id))\
                    .execute()

                if context_result.data:
                    context = context_result.data[0]
                    print("   📋 Context now exists:")
                    print(f"      📝 Title: {context.get('title', 'None')}")
                    print(f"      📊 Messages: {context.get('total_messages', 0)}")
            else:
                print("   ❌ Manual context creation failed!")

    except Exception as exc:
        print(f"   ❌ Error checking context: {exc}")

    # Test 2: Add another Q&A pair and verify context updates
    print("\n3. ➕ Adding another Q&A pair:")

    pair_id_2 = ConversationHistory.save_question_answer_pair(
        conversation_id=conversation_id,
        user_id=user_id,
        question="How often should I water tomatoes?",
        answer="Water tomatoes deeply 2-3 times per week, ensuring soil stays consistently moist."
    )

    print(f"   ✅ Saved second Q&A pair: {pair_id_2}")

    # Check updated context
    try:
        context_result = supabase.table("chat_context")\
            .select("*")\
            .eq("conversation_id", str(conversation_id))\
            .execute()

        if context_result.data:
            context = context_result.data[0]
            print("   📊 Updated context:")
            print(f"      📝 Title: {context.get('title', 'None')}")
            print(f"      📊 Total Messages: {context.get('total_messages', 0)} (should be 4)")
            print(f"      🕒 Last Activity: {context.get('last_activity', 'None')}")
        else:
            print("   ❌ Context record still missing!")

    except Exception as exc:
        print(f"   ❌ Error checking updated context: {exc}")

    # Test 3: Test get_user_conversations to see if it finds the context
    print("\n4. 👤 Testing get_user_conversations:")

    try:
        user_conversations = ConversationHistory.get_user_conversations(user_id, limit=10)
        print(f"   📈 Found {len(user_conversations)} conversations for {user_id}")

        for conv in user_conversations:
            if str(conv['conversation_id']) == str(conversation_id):
                print("   ✅ Test conversation found in user conversations!")
                print(f"      📝 Title: {conv.get('title', 'None')}")
                print(f"      💬 First Question: {conv.get('first_question', 'None')}")
                print(f"      📊 Message Count: {conv.get('message_count', 0)}")
                break
        else:
            print("   ❌ Test conversation NOT found in user conversations!")

    except Exception as exc:
        print(f"   ❌ Error testing get_user_conversations: {exc}")

    print("\n🎯 SUMMARY:")
    print("   If you see context records with proper data, the chat_context table is working!")
    print("   If you see errors or missing data, there's still an issue to fix.")

if __name__ == "__main__":
    test_chat_context_updates()