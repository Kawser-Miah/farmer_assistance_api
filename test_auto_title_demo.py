"""
Demo: Auto Title Generation Feature
Shows how conversation titles are automatically generated from first question.
"""

# Example API Request (First message in conversation):
example_request = {
    "query": "How to treat fungal disease in tomato plants during rainy season?",
    "user_id": "user123",
    "conversation_id": None,  # New conversation
    "conversation_history": None
}

# What happens internally:
# 1. System detects: conversation_history is None or empty (new conversation)
# 2. System calls: ConversationHistory.generate_conversation_title(first_question)
# 3. Gemini receives prompt:
"""
Based on this user question about farming/agriculture, generate a concise, descriptive title for this conversation.

User Question: "How to treat fungal disease in tomato plants during rainy season?"

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

# 4. Gemini generates: "Tomato Fungal Disease Treatment"
# 5. Title saved to chat_context table
# 6. Title returned in API response

# Example API Response:
example_response = {
    "answer": "For fungal diseases in tomatoes during rainy season, apply copper-based fungicide...",
    "sources": [{"content": "Fungal disease management in tomato crops..."}],
    "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
    "conversation_history": [
        {
            "role": "user",
            "content": "How to treat fungal disease in tomato plants during rainy season?",
            "timestamp": "2026-03-22T10:00:00Z"
        },
        {
            "role": "assistant",
            "content": "For fungal diseases in tomatoes during rainy season, apply copper-based fungicide...",
            "timestamp": "2026-03-22T10:00:05Z"
        }
    ],
    "conversation_title": "Tomato Fungal Disease Treatment"  # 🎯 AI-Generated Title!
}

print("✅ Auto Title Generation Complete!")
print("📝 First question → Gemini → Smart title")
print("🗂️ Perfect for conversation organization")
print("⚡ Works automatically on first message")