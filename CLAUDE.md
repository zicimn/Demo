# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Activate virtual environment (required before any Python commands)
source .venv/Scripts/activate

# Run the FastAPI development server (run from the repository root)
python app/main.py
# or equivalently, with app/ as the import root:
uvicorn main:app --app-dir app --reload --host 0.0.0.0 --port 8000

# Install/update dependencies
pip install -r requirements.txt

# Freeze current dependencies
pip freeze > requirements.txt
```

## Project Overview

A FastAPI backend for managing AI model metadata — providers, model specifications, capabilities, and pricing. Currently in early development (`app/main.py` is empty; models and config are scaffolded).

## Tech Stack

- **Framework:** FastAPI (async)
- **ORM:** SQLAlchemy 2.0 with async sessions (aiomysql driver)
- **Database:** MySQL 8+ (utf8mb4)
- **Cache:** Redis (async via `redis.asyncio`), domain-versioned cache keys
- **Auth/Security:** python-jose (JWT), passlib + argon2/bcrypt, itsdangerous
- **Validation:** Pydantic v2 + pydantic-settings + email-validator
- **Other:** APScheduler (scheduling), Sentry (error tracking), Cloudinary (media)

## Architecture

### Import convention (important)

`app/` is the **import root**, not a package — there is no `app/__init__.py`. Top-level
packages inside it are `api`, `services`, `models`, `schema`, `config`, plus the modules
`deps.py`, `err.py` and `main.py`.

- Use **absolute imports rooted at `app/`**: `from services.home import HomeService`,
  `from config.db import Base`, `from err import NotFound`.
- **Never use parent-relative imports** (`from ..err import ...`). Because `app/` is the
  import root, `services` is already a top-level package, so `..` goes beyond the
  top-level package and raises `ImportError: attempted relative import beyond top-level
  package` at startup. Relative imports *within* the same package (`from .model import X`
  in `services/__init__.py`) are fine.

### Directory Layout

```
app/
  main.py               # FastAPI app entry point (to be implemented)
  config/
    __init__.py          # Re-exports: redis_client, AsyncSessionLocal, logger, etc.
    db.py                # Async SQLAlchemy engine, session factory, get_db dependency
    cache.py             # Async Redis client, domain-versioned caching utils
    security.py          # Loads ASYNC_DATABASE_URL from .env
    logger.py            # File + console logger
  model/
    aimodel.py           # Ai_Model ORM model (maps to ai_model table)
    aimodelfunc.py       # Ai_Model_Func ORM model (maps to ai_model_func table)
    provider.py          # (placeholder)
    aimodelprice.py      # (placeholder)
  .env                  # Database connection string (gitignored)
sql/
  create.sql            # Full DDL (the authoritative schema reference)
```

### Domain Model (from `sql/create.sql`)

The domain revolves around **model providers** and their **models**:

- **`ai_provider`** — A vendor like DeepSeek, OpenAI. Each provider has a unique `provider_code`.
- **`ai_provider_endpoint`** — API endpoints per provider, keyed by `api_format` (e.g., `openai`, `anthropic`). A provider can serve multiple API formats.
- **`ai_model`** — A specific model under a provider. Tracks context length, max output, thinking mode support (`none`/`non_thinking_only`/`thinking_only`/`both`), and concurrency limits.
- **`ai_model_capability`** — Per-model capabilities: `json_output`, `tool_calls`, `image_understanding`, etc. Each has a `support_status` and optional `is_beta` flag.
- **`ai_model_price`** — Pricing entries per model, segmented by `price_type` (input/output/cache hit) and `time_period` (peak/off-peak), with effective date ranges.

The Python ORM models under `app/model/` partially mirror this schema — notably `Ai_Model_Func` corresponds to what the SQL calls `ai_model_capability` but uses a different naming convention. The SQL DDL is the source of truth.

### Caching Layer (`app/config/cache.py`)

Redis-backed caching with **domain-level version keys** — incrementing a version counter (e.g., `gal_version`) invalidates all cache entries for that domain without flushing unrelated keys. Key format: `prefix:v{VERSION}:arg1:arg2=val`. Supports TTL-based expiration and pattern-based deletion.

### Database Session Pattern

The `get_db()` async generator in `config/db.py` yields an `AsyncSession`, commits on success, rolls back on exception. Use it as a FastAPI dependency:

```python
from config.db import get_db

@router.get("/models")
async def list_models(db: AsyncSession = Depends(get_db)):
    ...
```

### Notable Gaps (Early Stage)

- `app/main.py` is empty — no app factory, router mounts, middleware, or lifespan handlers exist yet.
- `app/model/provider.py` and `app/model/aimodelprice.py` are empty stubs.
- No API routes, schemas (Pydantic request/response models), or service layer exist.
- No tests, no CI configuration.