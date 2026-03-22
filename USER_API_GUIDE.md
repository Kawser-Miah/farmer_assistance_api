# 🚀 **User-Level Conversation History API Guide**

This guide shows you how to use the improved conversation history system with proper question-answer linking.

## 🗄️ **Database Setup**

### Option 1: Fresh Installation
Run the SQL from `database_schema_improved.sql` in your Supabase SQL editor.

### Option 2: Upgrade Existing System
Run the `migration_script.sql` to upgrade your current database without losing data.

## 📡 **API Endpoints for Users**

### 1. **Start a New Chat Conversation**

**POST** `/ai-chat/chat`

```json
{
  "query": "What is the best fertilizer for tomatoes?",
  "user_id": "farmer123"
  // No conversation_id = new conversation
}
```

**Response:**
```json
{
  "answer": "For tomatoes, use a balanced fertilizer with NPK ratio 10-10-10...",
  "sources": [...],
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### 2. **Continue an Existing Conversation**

**POST** `/ai-chat/chat`

```json
{
  "query": "How much should I apply per plant?",
  "user_id": "farmer123",
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response:**
```json
{
  "answer": "Apply 1-2 tablespoons per plant, as the AI remembers you asked about tomato fertilizer...",
  "sources": [...],
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### 3. **Get All Your Conversations**

**GET** `/ai-chat/conversations/{user_id}`

```bash
curl "http://localhost:8000/ai-chat/conversations/farmer123?limit=10"
```

**Response:**
```json
{
  "user_id": "farmer123",
  "conversations": [
    {
      "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
      "first_question": "What is the best fertilizer for tomatoes?",
      "last_activity": "2024-03-22T10:30:00Z",
      "message_count": 4,
      "total_pairs": 2
    },
    {
      "conversation_id": "661f9511-f39c-52e5-b827-557766551111",
      "first_question": "How to treat plant diseases?",
      "last_activity": "2024-03-21T15:20:00Z",
      "message_count": 6,
      "total_pairs": 3
    }
  ]
}
```

### 4. **Get Conversation History (Q&A Pairs)**

**GET** `/ai-chat/conversations/{user_id}/{conversation_id}`

```bash
curl "http://localhost:8000/ai-chat/conversations/farmer123/550e8400-e29b-41d4-a716-446655440000?limit=5"
```

**Response:**
```json
{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "pairs": [
    {
      "question": "What is the best fertilizer for tomatoes?",
      "answer": "For tomatoes, use a balanced fertilizer with NPK ratio 10-10-10...",
      "timestamp": "2024-03-22T10:15:00Z"
    },
    {
      "question": "How much should I apply per plant?",
      "answer": "Apply 1-2 tablespoons per plant, mixing it into the soil...",
      "timestamp": "2024-03-22T10:18:00Z"
    }
  ],
  "total_messages": 4
}
```

### 5. **Get Only Q&A Pairs (Clean Format)**

**GET** `/ai-chat/conversations/{user_id}/{conversation_id}/pairs`

```bash
curl "http://localhost:8000/ai-chat/conversations/farmer123/550e8400-e29b-41d4-a716-446655440000/pairs?limit=5&include_incomplete=false"
```

### 6. **Delete a Conversation**

**DELETE** `/ai-chat/conversations/{user_id}/{conversation_id}`

```bash
curl -X DELETE "http://localhost:8000/ai-chat/conversations/farmer123/550e8400-e29b-41d4-a716-446655440000"
```

**Response:**
```json
{
  "message": "Conversation deleted successfully"
}
```

## 🔍 **What Makes This Better?**

### ❌ **Old System Problems:**
```
Message 1: Q: What is crop rotation?
Message 2: A: Crop rotation is...
Message 3: Q: How often to rotate?
Message 4: A: Every 2-3 years...

❌ No explicit linking - timing issues could mix up Q&A
❌ Hard to query specific question-answer pairs
❌ Fragile ordering based on timestamps
```

### ✅ **New System Solutions:**

```sql
-- Each Q&A pair gets a unique link ID
message_pair_id: abc123 | Q: What is crop rotation?
message_pair_id: abc123 | A: Crop rotation is...

message_pair_id: def456 | Q: How often to rotate?
message_pair_id: def456 | A: Every 2-3 years...

✅ Explicit Q&A linking in database
✅ Easy to query complete pairs
✅ Reliable ordering with sequence numbers
✅ User-friendly API endpoints
```

## 🧪 **Testing Examples**

### Test Script (Python):
```python
import requests
import json

base_url = "http://localhost:8000/ai-chat"
user_id = "test_user"

# 1. Start a conversation
response1 = requests.post(f"{base_url}/chat", json={
    "query": "What causes tomato blight?",
    "user_id": user_id
})
conv_id = response1.json()["conversation_id"]
print(f"Started conversation: {conv_id}")

# 2. Continue conversation
response2 = requests.post(f"{base_url}/chat", json={
    "query": "How do I prevent it?",
    "user_id": user_id,
    "conversation_id": conv_id
})
print(f"AI remembered context: {response2.json()['answer']}")

# 3. Get conversation history
history = requests.get(f"{base_url}/conversations/{user_id}/{conv_id}")
pairs = history.json()["pairs"]
print(f"Found {len(pairs)} Q&A pairs:")
for i, pair in enumerate(pairs, 1):
    print(f"  {i}. Q: {pair['question']}")
    print(f"     A: {pair['answer'][:100]}...")
```

## 💾 **Database Benefits**

- ✅ **Atomic Q&A pairing** - Questions and answers always linked
- ✅ **Fast queries** - Indexes on all important fields
- ✅ **Data integrity** - Database constraints prevent orphaned messages
- ✅ **Conversation metadata** - Auto-tracked message counts and timestamps
- ✅ **User isolation** - Each user's conversations are separate
- ✅ **Easy cleanup** - Delete entire conversations with one call

## 🔧 **Migration Support**

If you have existing data, the migration script will:
1. ✅ Backup your existing data
2. ✅ Add new columns safely
3. ✅ Link existing Q&A pairs automatically
4. ✅ Preserve all your conversation history
5. ✅ Update metadata and create indexes

**Ready to use the improved conversation system!** 🎉