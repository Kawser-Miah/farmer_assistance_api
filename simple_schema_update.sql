-- ==========================================
-- SIMPLE SUPABASE SCHEMA UPDATE
-- Add these columns manually in Supabase
-- ==========================================

-- 1. UPDATE EXISTING chat_messages TABLE
-- Copy and run these ALTER TABLE commands in your Supabase SQL editor:

ALTER TABLE chat_messages
ADD COLUMN user_id TEXT DEFAULT 'unknown',
ADD COLUMN message_pair_id UUID NULL,
ADD COLUMN sequence_number INTEGER DEFAULT 0;

-- 2. CREATE INDEXES for better performance
-- Run these in Supabase SQL editor:

CREATE INDEX IF NOT EXISTS idx_chat_messages_user_id ON chat_messages(user_id);
CREATE INDEX IF NOT EXISTS idx_chat_messages_pair_id ON chat_messages(message_pair_id);
CREATE INDEX IF NOT EXISTS idx_chat_messages_sequence ON chat_messages(conversation_id, sequence_number);

-- 3. UPDATE EXISTING chat_context TABLE
-- Add these columns to chat_context:

ALTER TABLE chat_context
ADD COLUMN user_id TEXT DEFAULT 'unknown',
ADD COLUMN title TEXT NULL,
ADD COLUMN total_messages INTEGER DEFAULT 0,
ADD COLUMN last_activity TIMESTAMP WITH TIME ZONE DEFAULT NOW();

-- ==========================================
-- HOW THE NEW SCHEMA WORKS:
-- ==========================================

-- BEFORE (your current table):
-- | id | conversation_id | role        | content           | created_at |
-- |----|-----------------|-------------|-------------------|------------|
-- | 1  | conv-123        | user        | What is farming?  | 10:00      |
-- | 2  | conv-123        | assistant   | Farming is...     | 10:01      |
-- | 3  | conv-123        | user        | How to plant?     | 10:05      |
-- | 4  | conv-123        | assistant   | To plant...       | 10:06      |

-- AFTER (with new columns):
-- | id | conversation_id | role      | content           | user_id | message_pair_id | sequence_number |
-- |----|-----------------|-----------|-------------------|---------|-----------------|-----------------|
-- | 1  | conv-123        | user      | What is farming?  | user1   | pair-001        | 1               |
-- | 2  | conv-123        | assistant | Farming is...     | system  | pair-001        | 2               |
-- | 3  | conv-123        | user      | How to plant?     | user1   | pair-002        | 3               |
-- | 4  | conv-123        | assistant | To plant...       | system  | pair-002        | 4               |

-- ✅ NOW QUESTIONS AND ANSWERS ARE PROPERLY LINKED BY message_pair_id!