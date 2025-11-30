# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Universal AI Wrapper is a FastAPI-based web API that provides a unified interface to interact with various AI models. It proxies requests through OpenRouter, enabling API key obfuscation, metadata enrichment, and logging capabilities.

## Development Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the FastAPI server
uvicorn app.server:app --reload

# Run the standalone main.py test script
cd app && python main.py
```

## Environment Variables

- `OPENROUTER_API_KEY` - Required for all AI model requests (set via devcontainer or .env)

## Architecture

```
app/
├── server.py              # FastAPI application with /chat/default endpoint
├── main.py                # Standalone test script for wrapper
├── models/
│   ├── chat_request_model.py   # Pydantic models: ChatRequest, Message, Role enum
│   └── chat_response_model.py  # WrapperResponse model with session tracking
├── wrappers/
│   ├── wrapperbase.py          # Abstract base class defining wrapper interface
│   └── pydantic_wrapper.py     # PydanticAIWrapper implementation using pydantic-ai
└── loggers/                    # Logging implementations (placeholder)
```

### Key Components

- **WrapperBase** (`app/wrappers/wrapperbase.py`): Abstract base class that defines the interface all AI wrappers must implement: `generate_text()`, `generate_stream()`, and properties for model, temperature, base_url, system_prompt.

- **PydanticAIWrapper** (`app/wrappers/pydantic_wrapper.py`): Current implementation using pydantic-ai's Agent with OpenAI-compatible provider. Supports both streaming and non-streaming responses.

- **Server** (`app/server.py`): FastAPI app exposing `/chat/default` POST endpoint that accepts ChatRequest and returns text or StreamingResponse.

### Request/Response Flow

1. Client sends POST to `/chat/default` with ChatRequest (model, messages, temperature, stream flag)
2. Server creates PydanticAIWrapper with hardcoded OpenRouter config
3. Wrapper formats messages and calls pydantic-ai Agent
4. Response returned as plain text or streamed chunks

## Security Note

The `.devcontainer/devcontainer.json` contains a hardcoded API key that should be removed and replaced with environment variable references only.