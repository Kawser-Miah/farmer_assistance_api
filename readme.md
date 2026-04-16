# Farmer Assistance Backend

Comprehensive user and developer documentation for the FastAPI backend in this repository.

This backend provides:
- Crop disease detection from image uploads
- AI farming chat with RAG (retrieval-augmented generation)
- Smart irrigation prediction
- Fertilizer recommendation
- Crop recommendation
- Crop yield estimation
- Commodity price prediction

It is designed for a Flutter/mobile client and uses Supabase for auth/data/storage plus local ML model assets for predictions.

## Table of Contents
- Project Overview
- Technology Stack
- Complete Repository Inventory (A to Z)
- Architecture and Request Flow
- Prerequisites
- Setup and Installation
- Environment Variables
- Supabase Requirements (Database, Storage, RPC)
- Running the API
- Authentication
- Full API Reference (All Endpoints)
- Request/Response Schema Reference
- ML Model Assets Reference
- AI Chat Conversation System Details
- Scripts and Testing Guide
- Existing Project Docs and SQL Files
- Troubleshooting
- Known Caveats and Current Behavior
- Production Readiness Checklist

## Project Overview

The application is a modular FastAPI server where each prediction domain follows the same pattern:

1. API router in `src/api`
2. Pydantic request/response models in `src/schemas`
3. Service prediction logic in `src/services/.../predict.py`
4. Lazy-loaded model/encoder files from `assets/`

For AI chat, an additional RAG pipeline is used:
- `sentence-transformers` for embeddings
- Supabase vector table + RPC for semantic retrieval
- Gemini (`gemini-2.5-flash`) for response generation and conversation title generation

## Technology Stack

- Python 3.x
- FastAPI + Uvicorn
- Pydantic / pydantic-settings
- TensorFlow (crop disease)
- scikit-learn/joblib/pickle-backed models
- XGBoost (price prediction model compatibility)
- OpenCV + NumPy
- Supabase Python client
- python-jose + requests for JWT validation
- google-genai + sentence-transformers + pypdf for AI chat and ingestion

Dependency note from verified repo memory:
- TensorFlow 2.21.0 had protobuf compatibility issues.
- `protobuf==6.31.1` is pinned and should remain pinned unless you retest TensorFlow compatibility.

## Complete Repository Inventory (A to Z)

### Top-level application, docs, SQL, scripts
- `.env`: local environment variables (contains Supabase and Google API keys)
- `.gitattributes`: LFS handling for model artifacts (`.h5`, `.pkl`, `.joblib`, `.csv`)
- `.gitignore`: ignores virtual env, caches, IDE files, env files, coverage, logs
- `AUTO_TITLE_GENERATION_GUIDE.md`: frontend integration notes for AI-generated conversation titles
- `auto_title_schema.sql`: adds `title` to `chat_context`
- `CHAT_CONTEXT_FIXED.md`: notes on fixing `chat_context` update behavior
- `CONVERSATION_OPTIMIZATION_COMPLETE.md`: notes on client-side conversation history optimization
- `demo_auto_titles.py`: demonstrates title generation behavior
- `demo_full_conversation_display.py`: demonstrates full conversation response payload
- `fix_chat_context_schema.sql`: SQL fix for `chat_context` nullable/required fields
- `FULL_CONVERSATION_DISPLAY_COMPLETE.md`: notes on returning full conversation in chat response
- `IMPLEMENTATION_GUIDE.md`: step-by-step integration note (historical)
- `INTEGRATION_COMPLETE.md`: integration summary for Q&A pairing
- `migration_script.sql`: migration for pairing and metadata columns
- `optimized_conversation_examples.py`: examples for sending conversation history from client
- `PRICE_PREDICTION_IMPLEMENTATION.md`: price module implementation summary
- `quick_test.py`: quick numpy-based fertilizer model inference script
- `requirements.txt`: runtime dependencies
- `run.py`: CLI entrypoint for starting Uvicorn
- `SCHEMA_FIX_GUIDE.md`: guide for fixing `chat_context` summary constraint
- `simple_schema_update.sql`: simplified schema migration commands
- `test_auto_title_demo.py`: auto-title demonstration test
- `test_auto_title_generation.py`: title generation tests
- `test_auto_title_integration.py`: title generation integration checks
- `test_chat_context.py`: chat context update test
- `test_conversation_example.py`: conversation API usage examples
- `test_fertilizer_api.py`: fertilizer endpoint request example
- `test_full_conversation_api.py`: full conversation response test
- `test_numpy_fertilizer.py`: extensive direct-model fertilizer tests
- `test_optimization.py`: conversation optimization tests
- `test_price_prediction.py`: direct price prediction test
- `test_qa_pairing_demo.py`: Q&A pairing demonstration
- `test_simple_context.py`: quick `chat_context` sanity test
- `title_generation_flow.py`: title generation behavior walkthrough
- `USER_API_GUIDE.md`: user-level API documentation (partially historical)
- `.vscode/settings.json`: workspace Python interpreter and analysis extra paths
- `database/migrations/`: migration folder (currently empty)

### Application source (`src/`)
- `src/main.py`: FastAPI app construction, middleware, router registration, root/health
- `src/core/config.py`: all settings, model paths, prefixes, env loading
- `src/core/database.py`: Supabase client initialization
- `src/core/jwt_validation.py`: Supabase JWT decode/verify via JWKS

#### API routers (`src/api/`)
- `ai_chat.py`
- `crop_disease_detection.py`
- `crop_recommendation.py`
- `fertilizer_tips.py`
- `price_predection.py`
- `smart_irrigation.py`
- `yield_estimation.py`

#### Schemas (`src/schemas/`)
- `ai_chat_schemas.py`
- `crop_disease_schemas.py`
- `crop_recommendation_schemas.py`
- `fertilizer_tips_schemas.py`
- `price_predection_schemas.py`
- `smart_irrigation_schemas.py`
- `yield_estimation_schemas.py`

#### Services (`src/services/`)
- `ai_chat/ai_chat_base.py`: orchestrates RAG + Gemini + history save
- `ai_chat/conversation_history.py`: conversation persistence, pairing, metadata, title generation
- `ai_chat/exceptions.py`: typed service errors
- `ai_chat/rag/embeddings.py`: embedding generation
- `ai_chat/rag/gemini_client.py`: Gemini client + prompt handling
- `ai_chat/rag/ingest.py`: document ingestion loop
- `ai_chat/rag/vector_store.py`: insert/search document operations
- `crop_recommendation/model.py`, `predict.py`
- `disease/model.py`, `predict.py`, `preprocess.py`, `crud_operation.py`
- `fertilizer_tips_service/model.py`, `predict.py`
- `price_predection/model.py`, `predict.py`
- `smart_irrigation_services/model.py`, `predict.py`
- `yield_estimation_service/model.py`, `predict.py`

### Assets and runtime output
- `assets/crop_disease_detection_ml_model.h5`: TensorFlow crop disease model
- `assets/crop_disease_detection_class_names.json`: disease class list
- `assets/best_irrigation_model.pkl`, `le_soil.pkl`, `le_crop.pkl`, `le_stage.pkl`
- `assets/fertilizer_model.pkl`, `fertilizer_encoder.pkl`, `crop_encoder.pkl`, `soil_encoder.pkl`
- `assets/yield_model.pkl`, `item_encoder.pkl`, `area_encoder.pkl`
- `assets/crop_recommendation_model.pkl`
- `assets/price_predection.pkl` (bundle with model + encoders + feature list)
- `media/gradcam/...png`: generated heatmap images (sample output)

## Architecture and Request Flow

### Standard ML endpoints
1. Client sends JSON (or multipart file for disease detection)
2. JWT dependency validates Supabase token (for protected routes)
3. Schema validation runs
4. `run_in_threadpool` calls prediction function
5. Prediction service lazy-loads model/encoders and predicts
6. API returns typed response

### AI chat endpoint
1. Receives query + optional `conversation_id` + optional `conversation_history`
2. Embeds query using `all-MiniLM-L6-v2`
3. Retrieves top documents from Supabase RPC (`match_documents`)
4. Builds prompt with retrieved context + previous conversation context
5. Calls Gemini (`gemini-2.5-flash`)
6. Saves Q&A pair to `chat_messages` with shared `message_pair_id`
7. Updates `chat_context` metadata and title
8. Returns answer + sources + updated conversation payload

## Prerequisites

- Linux/macOS/Windows with Python 3.10+
- pip and virtualenv support
- Access to Supabase project (URL and keys)
- Access to Gemini API key for AI chat
- Model files present in `assets/`

## Setup and Installation

```bash
# 1) Create virtual environment
python -m venv .venv

# 2) Activate environment (Linux/macOS)
source .venv/bin/activate

# 3) Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

## Environment Variables

Create `.env` in project root:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_KEY=your_service_role_key
GOOGLE_API_KEY=your_google_api_key
```

Important:
- `SUPABASE_SERVICE_KEY` is defined in settings but not actively used by runtime code shown.
- Rotate keys if real credentials were committed or shared.

## Supabase Requirements (Database, Storage, RPC)

### Minimum expected tables

#### 1) `chat_messages`
Expected columns used by code:
- `id`
- `conversation_id` (uuid)
- `user_id` (text)
- `role` (`user` or `assistant`)
- `content` (text)
- `message_pair_id` (uuid, nullable)
- `sequence_number` (integer)
- `created_at` (timestamp)

#### 2) `chat_context`
Expected columns used by code:
- `conversation_id` (uuid, PK)
- `user_id` (text)
- `title` (text)
- `summary` (nullable text)
- `total_messages` (integer)
- `last_activity` (timestamp)
- `created_at` (timestamp)
- `updated_at` (timestamp)

#### 3) `documents`
Expected columns:
- `content` (text)
- `embedding` (vector)

#### 4) `crop_disease_predictions`
Expected insert fields:
- `user_id`
- `label`
- `confidence`
- `heatmap_path`

#### 5) `users`
Used by debug endpoint `/crop-disease/test-users`.

### Required storage bucket
- Supabase Storage bucket name: `crop_disease`
- Used for Grad-CAM image upload/public URL retrieval

### Required RPC function for vector search
The code calls:
- `match_documents(query_embedding, match_count)`

Example implementation pattern (adjust table/columns as needed):

```sql
create extension if not exists vector;

-- Example assumes 384-d embeddings for all-MiniLM-L6-v2
-- Adjust dimensions if using another embedding model.

create or replace function match_documents(
  query_embedding vector(384),
  match_count int default 5
)
returns table (
  id bigint,
  content text,
  similarity float
)
language sql stable
as $$
  select
    d.id,
    d.content,
    1 - (d.embedding <=> query_embedding) as similarity
  from documents d
  order by d.embedding <=> query_embedding
  limit match_count;
$$;
```

### Migration helpers in this repo
- `simple_schema_update.sql`
- `migration_script.sql`
- `fix_chat_context_schema.sql`
- `auto_title_schema.sql`

Run the one matching your current database state.

## Running the API

```bash
# development mode with auto reload
python run.py --reload

# custom host/port
python run.py --host 0.0.0.0 --port 8080 --reload
```

Open:
- Swagger: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Authentication

Most business endpoints require:

```http
Authorization: Bearer <SUPABASE_USER_JWT>
```

Token validation details:
- JWKS is fetched from `SUPABASE_URL/auth/v1/.well-known/jwks.json`
- JWT is verified with algorithm `ES256`
- audience: `authenticated`
- issuer: `<SUPABASE_URL>/auth/v1`

Currently unprotected endpoints in code:
- `GET /`
- `GET /health`
- `GET /crop-disease/test-users`
- `POST /ai-chat/ingest`

## Full API Reference (All Endpoints)

### 1) System

#### `GET /`
Returns service metadata.

#### `GET /health`
Returns health status.

### 2) Crop Disease Detection

#### `POST /crop-disease/detect` (JWT required)
- Content type: `multipart/form-data`
- Field: `image` (`jpg`, `jpeg`, `png`)

Example:

```bash
curl -X POST "http://localhost:8000/crop-disease/detect" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -F "image=@/path/to/leaf.jpg"
```

Response shape:

```json
{
  "label": "Tomato_Late_blight",
  "confidence": 96.42,
  "heatmap_url": "https://.../storage/v1/object/public/crop_disease/gradcam_xxx.png"
}
```

What happens internally:
- Image is preprocessed for ResNet50 input
- Model predicts class
- Grad-CAM heatmap is generated from layer `conv5_block3_out`
- Heatmap image is uploaded to Supabase bucket `crop_disease`
- Prediction is saved in `crop_disease_predictions`

#### `GET /crop-disease/test-users` (no JWT currently)
Debug endpoint to fetch records from `users` table.

### 3) AI Chat + RAG

#### `POST /ai-chat/chat` (JWT required)

Request body:

```json
{
  "query": "How can I treat powdery mildew in cucumber?",
  "conversation_id": null,
  "conversation_history": [
    {
      "role": "user",
      "content": "Previous question",
      "timestamp": "2026-04-16T10:00:00Z"
    },
    {
      "role": "assistant",
      "content": "Previous answer",
      "timestamp": "2026-04-16T10:00:03Z"
    }
  ]
}
```

Response body:

```json
{
  "answer": "Use sulfur-based fungicide and improve airflow around plants.",
  "sources": [
    { "content": "Powdery mildew appears as white powder on leaves." }
  ],
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "conversation_history": [
    {
      "role": "user",
      "content": "How can I treat powdery mildew in cucumber?",
      "timestamp": "2026-04-16T10:12:00.000000+00:00"
    },
    {
      "role": "assistant",
      "content": "Use sulfur-based fungicide and improve airflow around plants.",
      "timestamp": "2026-04-16T10:12:00.000000+00:00"
    }
  ],
  "conversation_title": "Cucumber Powdery Mildew Treatment"
}
```

Notes:
- If `conversation_id` is omitted, a new UUID is created.
- If client sends `conversation_history`, server uses it for context (faster).
- Otherwise server fetches recent conversation from DB.

#### `GET /ai-chat/conversations?limit=20` (JWT required)
Returns a list of conversation summaries for authenticated user.

#### `GET /ai-chat/conversations/{conversation_id}?limit=50` (JWT required)
Returns linked Q&A pairs and total message count.

#### `DELETE /ai-chat/conversations/{conversation_id}` (JWT required)
Deletes conversation messages and context.

#### `POST /ai-chat/ingest` (no JWT currently)
- Content type: `multipart/form-data`
- Field: `file` (`.txt` or `.pdf`)
- Max upload: 10 MB

Example:

```bash
curl -X POST "http://localhost:8000/ai-chat/ingest" \
  -F "file=@/path/to/knowledge_base.pdf"
```

Response:

```json
{
  "message": "Documents ingested successfully.",
  "chunks_ingested": 12
}
```

### 4) Smart Irrigation

#### `POST /smart-irrigation/predict` (JWT required)

Request:

```json
{
  "crop_id": "Wheat",
  "soil_type": "Clay Soil",
  "seedling_stage": "Vegetative Growth / Root or Tuber Development",
  "moi": 40.0,
  "temp": 30.0,
  "humidity": 60.0
}
```

Response:

```json
{
  "irrigation_needed": true,
  "recommendation": "Irrigation Needed",
  "confidence": 0.95,
  "feature_importance": {
    "moisture": 0.41,
    "temperature": 0.25,
    "humidity": 0.13
  }
}
```

### 5) Fertilizer Recommendation

#### `POST /fertilizer-tips/predict` (JWT required)

Request:

```json
{
  "crop": "Wheat",
  "soil_color": "Red",
  "temperature": 25.0,
  "nitrogen": 80.0,
  "potassium": 40.0,
  "phosphorus": 40.0,
  "rainfall": 100.0,
  "ph": 6.5
}
```

Response:

```json
{
  "fertilizer": "Urea",
  "confidence": 0.95,
  "feature_importance": {
    "Nitrogen": 0.47,
    "pH": 0.19,
    "Rainfall": 0.14
  }
}
```

### 6) Crop Recommendation

#### `POST /crop-recommendation/predict` (JWT required)

Request:

```json
{
  "nitrogen": 90.0,
  "phosphorus": 42.0,
  "potassium": 43.0,
  "temperature": 20.87,
  "humidity": 82.0,
  "ph": 6.5,
  "rainfall": 202.93
}
```

Response model in current schema:

```json
{
  "crop": "Jute",
  "confidence": 0.95
}
```

Implementation note:
- Service computes `feature_importance`, but current response schema does not expose it.

### 7) Yield Estimation

#### `POST /yield-estimation/predict` (JWT required)

Request:

```json
{
  "item": "Maize",
  "area": "Brazil",
  "rainfall": 1300.0,
  "temperature": 28.5,
  "pesticides": 1800.0
}
```

Response:

```json
{
  "predicted_yield": 5.2,
  "yield_unit": "t/ha",
  "item": "Maize",
  "area": "Brazil",
  "confidence": 0.85,
  "feature_importance": {
    "Rainfall": 0.37,
    "Item": 0.28,
    "Pesticides": 0.16
  }
}
```

Unit conversion note:
- Model output is interpreted as `hg/ha` then converted to `t/ha` using `/10000`.

### 8) Price Prediction

#### `POST /price-prediction/predict` (JWT required)

Request:

```json
{
  "date": "2025-09-15",
  "admin1": "Dhaka",
  "admin2": "Dhaka",
  "market": "Dhaka (Karwan Bazar)",
  "latitude": 23.81,
  "longitude": 90.41,
  "category": "cereals and tubers",
  "commodity": "Rice (coarse)",
  "unit": "KG",
  "priceflag": "actual",
  "pricetype": "Retail"
}
```

Response:

```json
{
  "predicted_price": 51.59,
  "commodity": "Rice (coarse)",
  "market": "Dhaka (Karwan Bazar)",
  "unit": "KG",
  "date": "2025-09-15"
}
```

Feature engineering done internally:
- `year`, `month`, `quarter`
- `month_sin`, `month_cos`
- categorical label encodings
- unknown categories mapped to `-1`

## Request/Response Schema Reference

### AI Chat
- `ChatRequest`
  - `query`: string, 1..2000
  - `conversation_id`: optional UUID
  - `conversation_history`: optional list of `{role, content, timestamp}`
- `ChatResponse`
  - `answer`: string
  - `sources`: list of source objects
  - `conversation_id`: UUID
  - `conversation_history`: list of chat messages
  - `conversation_title`: optional string

### Crop Disease
- Response: `{label: str, confidence: float, heatmap_url: str}`

### Crop Recommendation
- Request: N, P, K, temperature, humidity, pH, rainfall
- Response: crop + confidence

### Fertilizer
- Request: crop, soil_color, temperature, N, K, P, rainfall, pH
- Response: fertilizer + confidence + feature_importance

### Smart Irrigation
- Request: crop_id, soil_type, seedling_stage, moi, temp, humidity
- Response: irrigation_needed + recommendation + confidence + feature_importance

### Yield
- Request: item, area, rainfall, temperature, pesticides
- Response: predicted_yield + yield_unit + item + area + confidence + feature_importance

### Price
- Request: date/location/market/product fields
- Response: predicted_price + context fields

## ML Model Assets Reference

| File | Used By | Purpose |
|---|---|---|
| `crop_disease_detection_ml_model.h5` | disease service | TensorFlow disease classification |
| `crop_disease_detection_class_names.json` | disease service | class labels |
| `best_irrigation_model.pkl` | smart irrigation | irrigation classifier |
| `le_soil.pkl`, `le_crop.pkl`, `le_stage.pkl` | smart irrigation | encoders for categorical inputs |
| `fertilizer_model.pkl` | fertilizer | fertilizer classifier |
| `fertilizer_encoder.pkl` | fertilizer | output decoder |
| `crop_encoder.pkl`, `soil_encoder.pkl` | fertilizer | input encoders |
| `yield_model.pkl` | yield estimation | yield regression model |
| `item_encoder.pkl`, `area_encoder.pkl` | yield estimation | input encoders |
| `crop_recommendation_model.pkl` | crop recommendation | crop classifier |
| `price_predection.pkl` | price prediction | bundle with model + encoders + feature list |

## AI Chat Conversation System Details

### Q&A pairing
- Each question/answer pair is saved with one shared `message_pair_id`.
- Sequence order is maintained with `sequence_number`.

### Metadata updates
After each pair save, code updates:
- total message count
- last activity timestamp
- title generation for new conversation

### Auto title generation
- Runs only for new conversation contexts.
- Uses Gemini prompt to create 3-8 word descriptive title.
- If generation fails, fallback uses truncated first question words.

### Performance optimization
- If client sends `conversation_history`, the server avoids DB read for context.
- This reduces latency for ongoing chat sessions.

## Scripts and Testing Guide

These scripts are in repository root.

### API and feature verification
```bash
python test_fertilizer_api.py
python test_price_prediction.py
python test_full_conversation_api.py
python test_optimization.py
python test_chat_context.py
python test_simple_context.py
python test_qa_pairing_demo.py
python test_auto_title_generation.py
python test_auto_title_integration.py
python test_auto_title_demo.py
python test_conversation_example.py
```

### Local model direct tests/demos
```bash
python quick_test.py
python test_numpy_fertilizer.py
python demo_auto_titles.py
python demo_full_conversation_display.py
python optimized_conversation_examples.py
python title_generation_flow.py
```

Notes:
- Many scripts require valid Supabase and/or Gemini credentials.
- Some scripts are demonstration-style and not strict unit tests.

## Existing Project Docs and SQL Files

The repo already contains detailed historical notes. This `readme.md` is the consolidated, code-accurate reference.

Use these for migration background and implementation history:
- `USER_API_GUIDE.md`
- `IMPLEMENTATION_GUIDE.md`
- `INTEGRATION_COMPLETE.md`
- `FULL_CONVERSATION_DISPLAY_COMPLETE.md`
- `CONVERSATION_OPTIMIZATION_COMPLETE.md`
- `AUTO_TITLE_GENERATION_GUIDE.md`
- `SCHEMA_FIX_GUIDE.md`
- `CHAT_CONTEXT_FIXED.md`
- `PRICE_PREDICTION_IMPLEMENTATION.md`

SQL utilities:
- `simple_schema_update.sql`
- `migration_script.sql`
- `fix_chat_context_schema.sql`
- `auto_title_schema.sql`

## Troubleshooting

### 1) JWT decode fails on startup
- Ensure `SUPABASE_URL` is valid.
- `jwt_validation.py` fetches JWKS during import; network and URL must be available.

### 2) `chat_context.summary` NOT NULL error
- Apply `fix_chat_context_schema.sql` or manual alter:

```sql
alter table chat_context alter column summary drop not null;
```

### 3) AI chat errors about missing Gemini key
- Set `GOOGLE_API_KEY` in `.env`.

### 4) Price prediction bundle errors
- Ensure `assets/price_predection.pkl` exists and is compatible.
- Confirm `xgboost` is installed (already in `requirements.txt`).

### 5) TensorFlow/protobuf runtime errors
- Keep `protobuf==6.31.1` (pinned in `requirements.txt`).

### 6) Disease detection fails on image upload
- Use JPEG/PNG only.
- Ensure image is valid and non-empty.

### 7) Ingest endpoint returns empty content
- PDF may have no extractable text layer.
- Try text-based PDF or `.txt` file.

## Known Caveats and Current Behavior

- Naming typo exists in module paths: `price_predection` (kept as-is across codebase).
- `GET /crop-disease/test-users` is currently open (no JWT dependency).
- `POST /ai-chat/ingest` is currently open (no JWT dependency).
- Root endpoint currently reports `crop-disease` predict path as `/predict`, while actual route is `/detect`.
- Some older docs/scripts show `user_id` in chat request body; current API takes `user_id` from JWT dependency for protected routes.
- `src/schemas/ai_chat_schemas.py` contains duplicate import lines (non-breaking, but cleanup recommended).

## Production Readiness Checklist

- Restrict CORS origins in `src/core/config.py` (currently `['*']`).
- Protect currently open endpoints (`/ai-chat/ingest`, `/crop-disease/test-users`) if required.
- Replace debug `detail=str(e)` 500 responses with safer generic messages where needed.
- Rotate secrets and remove real keys from `.env` before sharing/deploying.
- Add automated test suite (pytest-based) and CI pipeline.
- Add rate limiting and request logging/monitoring.
- Validate Supabase row-level security policies for all tables.

---

If you use this backend from Flutter, the recommended client strategy is:
1. Authenticate user with Supabase.
2. Send JWT in `Authorization` header for protected endpoints.
3. For AI chat, keep local `conversation_history` state and send it back on each message.
4. Render `conversation_title` in chat list and `conversation_history` directly in chat view.
