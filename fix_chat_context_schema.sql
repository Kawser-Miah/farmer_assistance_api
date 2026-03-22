-- =============================================
-- CHAT_CONTEXT TABLE SCHEMA FIX
-- Run these commands in your Supabase SQL Editor
-- =============================================

-- 1. FIRST: Check your current table structure
-- Run this to see what columns you currently have:
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'chat_context'
ORDER BY ordinal_position;

-- =============================================
-- 2. EXPECTED CURRENT STRUCTURE (what you probably have):
-- =============================================
-- conversation_id UUID PRIMARY KEY
-- summary TEXT NOT NULL  ← This is causing the error!
-- updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()

-- =============================================
-- 3. REQUIRED STRUCTURE (what my code needs):
-- =============================================
-- conversation_id UUID PRIMARY KEY
-- user_id TEXT NOT NULL
-- title TEXT NULL (optional)
-- summary TEXT NULL (make it optional, not required)
-- total_messages INTEGER DEFAULT 0
-- last_activity TIMESTAMP WITH TIME ZONE DEFAULT NOW()
-- created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
-- updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()

-- =============================================
-- 4. FIX COMMANDS - Run these step by step:
-- =============================================

-- Step 1: Make summary column nullable (this fixes the immediate error)
ALTER TABLE chat_context ALTER COLUMN summary DROP NOT NULL;

-- Step 2: Add missing columns if they don't exist
ALTER TABLE chat_context
ADD COLUMN IF NOT EXISTS user_id TEXT DEFAULT 'unknown',
ADD COLUMN IF NOT EXISTS title TEXT NULL,
ADD COLUMN IF NOT EXISTS total_messages INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS last_activity TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();

-- Step 3: Update existing records to have default values
UPDATE chat_context
SET
    user_id = COALESCE(user_id, 'unknown'),
    total_messages = COALESCE(total_messages, 0),
    last_activity = COALESCE(last_activity, NOW()),
    created_at = COALESCE(created_at, NOW())
WHERE user_id IS NULL OR total_messages IS NULL;

-- Step 4: Make user_id required after setting defaults
ALTER TABLE chat_context ALTER COLUMN user_id SET NOT NULL;

-- =============================================
-- 5. VERIFY THE FIX - Run this to confirm structure:
-- =============================================
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'chat_context'
ORDER BY ordinal_position;

-- Expected columns after fix:
-- conversation_id | uuid | NO | uuid_generate_v4()
-- user_id | text | NO | 'unknown'::text
-- title | text | YES |
-- summary | text | YES |  ← Now nullable!
-- total_messages | integer | YES | 0
-- last_activity | timestamp with time zone | YES | now()
-- created_at | timestamp with time zone | YES | now()
-- updated_at | timestamp with time zone | YES | now()