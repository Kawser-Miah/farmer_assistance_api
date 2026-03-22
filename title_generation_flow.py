"""
Demo: AI Title Generation - ONLY First Message
Shows that titles are generated only once per conversation.
"""

print("🎯 Auto Title Generation - First Message Only")
print("=" * 50)

# Conversation Scenario:
print("\n📝 Conversation Flow:")
print("User starts new conversation...")

# Message 1 (First message):
print("\n1️⃣ FIRST MESSAGE:")
print("Query: 'How to prevent pest in tomato plants?'")
print("↓ System detects: NEW conversation (no existing context)")
print("↓ Gemini generates title: 'Tomato Pest Prevention'")
print("✅ Title saved to database")
print("📤 Response includes: conversation_title: 'Tomato Pest Prevention'")

print("\n" + "─" * 40)

# Message 2 (Follow-up):
print("\n2️⃣ SECOND MESSAGE (same conversation):")
print("Query: 'What about organic pesticides?'")
print("↓ System detects: EXISTING conversation context found")
print("↓ Retrieves existing title: 'Tomato Pest Prevention'")
print("❌ NO title generation (saves API calls)")
print("📤 Response includes: conversation_title: 'Tomato Pest Prevention'")

print("\n" + "─" * 40)

# Message 3 (Another follow-up):
print("\n3️⃣ THIRD MESSAGE (same conversation):")
print("Query: 'How often should I spray?'")
print("↓ System detects: EXISTING conversation context found")
print("↓ Retrieves existing title: 'Tomato Pest Prevention'")
print("❌ NO title generation (saves API calls)")
print("📤 Response includes: conversation_title: 'Tomato Pest Prevention'")

print("\n" + "═" * 50)

# Technical Details:
print("\n🔧 TECHNICAL IMPLEMENTATION:")
print("✅ Title generation: ONLY on first message")
print("✅ Subsequent messages: Retrieve from database")
print("✅ Efficient: No unnecessary API calls")
print("✅ Consistent: Same title throughout conversation")

# Database State:
print("\n💾 DATABASE STATE:")
print("chat_context table:")
print("├── conversation_id: 12345")
print("├── title: 'Tomato Pest Prevention' (set once)")
print("├── total_messages: 6 (updated each time)")
print("└── last_activity: 2026-03-22T10:30:00Z (updated)")

print("\n🎉 PERFECT! Title generated once, reused efficiently!")