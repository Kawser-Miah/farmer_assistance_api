"""
Example demonstrating how the enhanced chat API returns full conversation history for display.
This shows how your frontend/mobile app should handle the conversation display.
"""
import json

def show_enhanced_chat_api_example():
    """Demonstrate the enhanced API response with full conversation history."""

    print("=== ENHANCED CHAT API - FULL CONVERSATION DISPLAY ===")

    # Example API request
    print("\n1. 📱 FRONTEND SENDS REQUEST:")
    api_request = {
        "query": "How often should I water tomatoes?",
        "user_id": "farmer123",
        "conversation_id": "550e8400-e29b-41d4-a716-446655440000"
    }
    print(f"POST /ai-chat/chat")
    print(f"{json.dumps(api_request, indent=2)}")

    # Example enhanced API response
    print("\n2. 🚀 ENHANCED API RESPONSE:")
    api_response = {
        "answer": "Water tomatoes deeply 2-3 times per week, ensuring soil stays consistently moist but not waterlogged.",
        "sources": [
            {
                "content": "Tomatoes require consistent moisture to prevent blossom end rot and cracking."
            }
        ],
        "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
        "conversation_history": [
            {
                "role": "user",
                "content": "What is the best fertilizer for tomatoes?",
                "timestamp": "2024-03-22T10:30:00Z"
            },
            {
                "role": "assistant",
                "content": "For tomatoes, I recommend using a balanced fertilizer with NPK ratio 10-10-10 during early growth, then switch to a lower nitrogen fertilizer during fruiting.",
                "timestamp": "2024-03-22T10:30:05Z"
            },
            {
                "role": "user",
                "content": "How often should I water tomatoes?",
                "timestamp": "2024-03-22T10:35:00Z"
            },
            {
                "role": "assistant",
                "content": "Water tomatoes deeply 2-3 times per week, ensuring soil stays consistently moist but not waterlogged.",
                "timestamp": "2024-03-22T10:35:05Z"
            }
        ]
    }
    print(f"{json.dumps(api_response, indent=2)}")

    print("\n3. 📱 HOW FRONTEND DISPLAYS THIS:")
    print("┌─────────────────────────────────────────────────────┐")
    print("│                  CHAT INTERFACE                     │")
    print("├─────────────────────────────────────────────────────┤")

    # Display the conversation history
    for i, msg in enumerate(api_response["conversation_history"]):
        if msg["role"] == "user":
            print(f"│ 👤 You: {msg['content']}")
            print(f"│    {msg['timestamp']}")
        else:
            print(f"│ 🤖 AI: {msg['content'][:50]}{'...' if len(msg['content']) > 50 else ''}")
            print(f"│    {msg['timestamp']}")
        if i < len(api_response["conversation_history"]) - 1:
            print("│")

    print("└─────────────────────────────────────────────────────┘")

    print("\n4. 💡 BENEFITS FOR YOUR APP:")
    print("   ✅ Complete conversation history in one API call")
    print("   ✅ No need for separate history endpoint calls")
    print("   ✅ Always shows the latest conversation state")
    print("   ✅ Perfect for chat bubbles/message lists")
    print("   ✅ Timestamps for message ordering")
    print("   ✅ Role-based styling (user vs assistant)")

    print("\n5. 📲 MOBILE APP IMPLEMENTATION:")
    react_native_example = '''
// React Native Example
const ChatScreen = () => {
    const [messages, setMessages] = useState([]);

    const sendMessage = async (userMessage) => {
        const response = await fetch('/ai-chat/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                query: userMessage,
                user_id: currentUser.id,
                conversation_id: currentConversationId
            })
        });

        const data = await response.json();

        // Update the entire conversation display
        setMessages(data.conversation_history);
        setCurrentConversationId(data.conversation_id);
    };

    return (
        <FlatList
            data={messages}
            renderItem={({item}) => (
                <ChatBubble
                    message={item.content}
                    isUser={item.role === 'user'}
                    timestamp={item.timestamp}
                />
            )}
        />
    );
};
    '''
    print(react_native_example)

    print("\n6. 🌐 FLUTTER IMPLEMENTATION:")
    flutter_example = '''
// Flutter Example
class ChatScreen extends StatefulWidget {
  @override
  _ChatScreenState createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  List<ChatMessage> messages = [];
  String? conversationId;

  Future<void> sendMessage(String userMessage) async {
    final response = await http.post(
      Uri.parse('/ai-chat/chat'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'query': userMessage,
        'user_id': currentUser.id,
        'conversation_id': conversationId,
      }),
    );

    final data = jsonDecode(response.body);

    setState(() {
      messages = (data['conversation_history'] as List)
          .map((msg) => ChatMessage.fromJson(msg))
          .toList();
      conversationId = data['conversation_id'];
    });
  }

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      itemCount: messages.length,
      itemBuilder: (context, index) {
        final message = messages[index];
        return ChatBubble(
          message: message.content,
          isUser: message.role == 'user',
          timestamp: message.timestamp,
        );
      },
    );
  }
}
    '''
    print(flutter_example)

if __name__ == "__main__":
    show_enhanced_chat_api_example()