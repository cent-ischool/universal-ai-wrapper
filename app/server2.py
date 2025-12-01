from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.models.chat_request_model import ChatRequest
from app.models.chat_response_model import WrapperResponse
from app.models.ai_configuration_model import AIConfigurationModel, AIConfigurations
from app.wrappers.requests_wrapper import RequestsWrapper
import time
import uuid
from fastapi.responses import StreamingResponse
from pydantic_yaml import parse_yaml_raw_as
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional

if not load_dotenv(".env"):
    raise FileNotFoundError("Could not find .env file at .env")

app = FastAPI(title="Universal AI Wrapper API - Requests Implementation")

# Security scheme
security = HTTPBearer()

# Load configurations at startup
config_path = Path(__file__).parent / "config.yaml"
with open(config_path, "r") as f:
    yaml_content = f.read()
configurations = parse_yaml_raw_as(AIConfigurations, yaml_content)


# Create authentication dependency factory
def create_auth_dependency(expected_api_key: str):
    """Factory function to create an authentication dependency for a specific API key."""

    async def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
        """Verify that the provided API key matches the expected one."""
        if credentials.credentials != expected_api_key:
            raise HTTPException(
                status_code=401,
                detail="Invalid API key",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return credentials.credentials

    return verify_api_key


# Create dynamic routes for each configuration
def create_chat_endpoint(config_name: str, config : AIConfigurationModel):
    """Factory function to create a chat endpoint for a specific configuration."""

    # Endpoint is config_name 
    config.endpoint = config_name

    # Create authentication dependency for this endpoint
    auth_dependency = create_auth_dependency(config.api_key)

    async def chat_endpoint(
        request: ChatRequest,
        api_key: str = Depends(auth_dependency)
    ):
        """
        Handle chat requests using the {config_name} configuration.

        Args:
            request: ChatRequest containing messages and other parameters
            api_key: Verified API key from Authorization header

        Returns:
            Text response or streaming response
        """
        base_url: str = 'https://openrouter.ai/api/v1'
        stream = request.stream if request.stream is not None else False

        # Convert Pydantic Message objects to dictionaries
        messages = [{"role": msg.role.value, "content": msg.content} for msg in request.messages]

        # Use the requests wrapper with configuration settings
        provider = RequestsWrapper(config, base_url=base_url)

        if stream:
            async def stream_generator():
                async for chunk in provider.generate_stream(messages=messages):
                    yield chunk.encode("utf-8") if isinstance(chunk, str) else chunk

            return StreamingResponse(stream_generator(), media_type="text/event-stream")
        else:
            response_text = await provider.generate_text(messages=messages)
            return response_text

    # Set function name and docstring for better API docs
    chat_endpoint.__name__ = f"chat_endpoint_{config_name}"
    chat_endpoint.__doc__ = config.description

    return chat_endpoint


# Register dynamic routes for each configuration
for config_name, config in configurations.configurations.items():
    endpoint = create_chat_endpoint(config_name, config)
    app.post(
        f"/{config_name}/chat/completions",
        name=f"{config_name}_chat_completions",
        tags=["endpoints"]
    )(endpoint)


@app.get("/", tags=["system"])
async def root():
    """Root endpoint for health check."""
    return {"status": "ok", "message": "Universal AI Wrapper API is running (Requests Implementation)"}


@app.get("/health", tags=["system"])
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/configurations", tags=["system"])
async def list_configurations():
    """List all available configurations and their endpoints."""
    config_list = []
    for config_name, config in configurations.configurations.items():
        config_list.append({
            "name": config_name,
            "endpoint": f"/{config_name}/chat/completions",
            "model": config.model,
            "description": config.description,
            "temperature": config.temperature,
            "top_p": config.top_p,
            "requires_auth": True
        })
    return {"configurations": config_list}
