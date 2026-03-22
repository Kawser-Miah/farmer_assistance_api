"""
MIGRATION SCRIPT: From basic chat to proper Q&A paired chat system
Run this script to upgrade your existing chat_messages table to the new schema
"""

-- =================================================================
-- STEP 1: BACKUP YOUR EXISTING DATA (IMPORTANT!)
-- =================================================================
-- Run this first to backup your data:
-- CREATE TEMPORARY TABLE chat_messages_backup AS SELECT * FROM chat_messages;

-- =================================================================
-- STEP 2: ADD NEW COLUMNS TO EXISTING TABLE (Safe Migration)
-- =================================================================
-- Add new columns to existing table without losing data

ALTER TABLE chat_messages
ADD COLUMN IF NOT EXISTS message_pair_id UUID NULL,
ADD COLUMN IF NOT EXISTS user_id TEXT DEFAULT 'unknown',
ADD COLUMN IF NOT EXISTS parent_message_id UUID NULL,
ADD COLUMN IF NOT EXISTS sequence_number INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();

-- =================================================================
-- STEP 3: CREATE INDEXES
-- =================================================================
CREATE INDEX IF NOT EXISTS idx_chat_messages_conversation_id ON chat_messages(conversation_id);
CREATE INDEX IF NOT EXISTS idx_chat_messages_user_id ON chat_messages(user_id);
CREATE INDEX IF NOT EXISTS idx_chat_messages_message_pair_id ON chat_messages(message_pair_id);
CREATE INDEX IF NOT EXISTS idx_chat_messages_created_at ON chat_messages(created_at);

-- =================================================================
-- STEP 4: UPDATE EXISTING DATA TO HAVE PROPER PAIRS
-- =================================================================
-- This script will create message_pair_ids for existing Q&A pairs

DO $$
DECLARE
    conversation_record RECORD;
    message_record RECORD;
    current_pair_id UUID;
    current_sequence INTEGER;
    pending_question RECORD;
BEGIN
    -- Process each conversation
    FOR conversation_record IN
        SELECT DISTINCT conversation_id FROM chat_messages
    LOOP
        current_sequence := 1;
        pending_question := NULL;

        -- Process messages in chronological order
        FOR message_record IN
            SELECT id, role, content, created_at
            FROM chat_messages
            WHERE conversation_id = conversation_record.conversation_id
            ORDER BY created_at ASC
        LOOP
            IF message_record.role = 'user' THEN
                -- Start a new Q&A pair
                current_pair_id := gen_random_uuid();
                pending_question := message_record;

                -- Update the question with pair_id and sequence
                UPDATE chat_messages
                SET message_pair_id = current_pair_id,
                    sequence_number = current_sequence
                WHERE id = message_record.id;

                current_sequence := current_sequence + 1;

            ELSIF message_record.role = 'assistant' AND pending_question IS NOT NULL THEN
                -- Complete the pair
                UPDATE chat_messages
                SET message_pair_id = current_pair_id,
                    sequence_number = current_sequence
                WHERE id = message_record.id;

                current_sequence := current_sequence + 1;
                pending_question := NULL;
            END IF;
        END LOOP;

        RAISE NOTICE 'Processed conversation: %', conversation_record.conversation_id;
    END LOOP;
END $$;

-- =================================================================
-- STEP 5: UPDATE CHAT_CONTEXT TABLE
-- =================================================================
-- Update the chat_context table structure

ALTER TABLE chat_context
ADD COLUMN IF NOT EXISTS user_id TEXT DEFAULT 'unknown',
ADD COLUMN IF NOT EXISTS title TEXT NULL,
ADD COLUMN IF NOT EXISTS total_messages INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS total_pairs INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS last_activity TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();

-- Update existing context records with message counts
UPDATE chat_context
SET
    total_messages = (
        SELECT COUNT(*)
        FROM chat_messages cm
        WHERE cm.conversation_id = chat_context.conversation_id
    ),
    total_pairs = (
        SELECT COUNT(DISTINCT message_pair_id)
        FROM chat_messages cm
        WHERE cm.conversation_id = chat_context.conversation_id
        AND message_pair_id IS NOT NULL
    ),
    last_activity = (
        SELECT MAX(created_at)
        FROM chat_messages cm
        WHERE cm.conversation_id = chat_context.conversation_id
    );

-- =================================================================
-- STEP 6: CREATE THE ENHANCED DATABASE FUNCTIONS AND VIEWS
-- =================================================================
-- (Copy the content from database_schema_improved.sql starting from line 25)

-- =================================================================
-- STEP 7: VERIFY MIGRATION
-- =================================================================
-- Run these queries to verify everything worked:

-- Check Q&A pairs are properly linked
SELECT
    conversation_id,
    message_pair_id,
    role,
    LEFT(content, 50) as content_preview,
    sequence_number
FROM chat_messages
WHERE conversation_id = (SELECT conversation_id FROM chat_messages LIMIT 1)
ORDER BY sequence_number;

-- Check conversation metadata
SELECT * FROM chat_context LIMIT 5;

-- Test the new view
SELECT * FROM conversation_pairs LIMIT 5;