-- Add title column to chat_context table
ALTER TABLE chat_context ADD COLUMN title VARCHAR(100);

-- Make title column NOT NULL with a default
ALTER TABLE chat_context ALTER COLUMN title SET DEFAULT 'New Conversation';

-- Update existing conversations to have a default title
UPDATE chat_context SET title = 'New Conversation' WHERE title IS NULL;

-- Now make it required for new entries
ALTER TABLE chat_context ALTER COLUMN title SET NOT NULL;

-- Optional: Add index for faster title searches
CREATE INDEX idx_chat_context_title ON chat_context(title);

-- Example of what the final table looks like:
/*
Table: chat_context
Columns:
- conversation_id (UUID, PRIMARY KEY)
- title (VARCHAR(100), NOT NULL) -- NEW: Auto-generated title
- summary (TEXT, NULLABLE)
- updated_at (TIMESTAMP WITH TIME ZONE)
*/