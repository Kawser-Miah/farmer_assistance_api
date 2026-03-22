"""
Test script for the new auto title generation feature.
Demonstrates AI-powered conversation titles like Claude and other AI assistants.
"""

def test_auto_title_generation():
    """Test the AI-powered automatic title generation."""

    print("=== AUTO TITLE GENERATION TEST ===")

    # Test cases with different types of farming questions
    test_questions = [
        "How do I treat powdery mildew on my cucumber plants in the greenhouse?",
        "What's the best organic fertilizer for tomato seedlings?",
        "When should I plant corn in Iowa and what variety is best?",
        "My apple tree leaves are turning yellow, what could be wrong?",
        "How to set up drip irrigation for my vegetable garden?",
        "What are the signs of nitrogen deficiency in pepper plants?",
        "Best crop rotation schedule for small farm in California?",
        "How to prevent soil erosion on sloped farmland?",
        "Organic pest control methods for cabbage worms?",
        "When to harvest winter wheat and how to store it?"
    ]

    print("\n🧪 TESTING AI TITLE GENERATION:")
    print("━" * 80)

    try:
        from src.services.ai_chat.conversation_history import ConversationHistory

        for i, question in enumerate(test_questions, 1):
            print(f"\n{i:2d}. ❓ Question: {question}")

            # Generate title
            title = ConversationHistory.generate_conversation_title(question)

            print(f"    🎯 Generated Title: '{title}'")
            print(f"    📏 Length: {len(title)} characters")

    except ImportError:
        print("❌ Could not import ConversationHistory - check your imports")
        return
    except Exception as e:
        print(f"❌ Error during title generation: {e}")
        return

    print("\n" + "━" * 80)
    print("✅ AUTO TITLE GENERATION COMPLETE!")

    print("\n🎯 EXPECTED TITLE EXAMPLES:")
    expected_examples = [
        "Cucumber Powdery Mildew Treatment",
        "Organic Tomato Seedling Fertilizer",
        "Iowa Corn Planting Guide",
        "Apple Tree Yellow Leaves Diagnosis",
        "Vegetable Garden Drip Irrigation",
        "Pepper Plant Nitrogen Deficiency",
        "California Small Farm Crop Rotation",
        "Sloped Farmland Erosion Prevention",
        "Organic Cabbage Worm Control",
        "Winter Wheat Harvest Storage"
    ]

    for i, example in enumerate(expected_examples, 1):
        print(f"   {i:2d}. {example}")

    print("\n📱 API RESPONSE WITH AUTO TITLES:")
    print("""
    {
        "answer": "For cucumber powdery mildew, use sulfur-based fungicides...",
        "sources": [...],
        "conversation_id": "uuid-123",
        "conversation_title": "Cucumber Powdery Mildew Treatment",
        "conversation_history": [
            {
                "role": "user",
                "content": "How do I treat powdery mildew...",
                "timestamp": "2024-03-22T10:30:00Z"
            },
            {
                "role": "assistant",
                "content": "For cucumber powdery mildew...",
                "timestamp": "2024-03-22T10:30:05Z"
            }
        ]
    }
    """)

if __name__ == "__main__":
    test_auto_title_generation()