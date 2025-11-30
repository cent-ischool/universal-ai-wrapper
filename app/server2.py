from fastapi import FastAPI
from app.models.chat_request_model import ChatRequest
from app.models.chat_response_model import WrapperResponse
from app.models.ai_configuration_model import AIConfigurations
from app.wrappers.requests_wrapper import RequestsWrapper
import time
import uuid
from fastapi.responses import StreamingResponse
from pydantic_yaml import parse_yaml_raw_as
from pathlib import Path
from dotenv import load_dotenv

if not load_dotenv(".env"):
    raise FileNotFoundError("Could not find .env file at .env")

app = FastAPI(title="Universal AI Wrapper API - Requests Implementation")

# Load configurations at startup
config_path = Path(__file__).parent / "config.yaml"
with open(config_path, "r") as f:
    yaml_content = f.read()
configurations = parse_yaml_raw_as(AIConfigurations, yaml_content)


# Create dynamic routes for each configuration
def create_chat_endpoint(config_name: str, config):
    """Factory function to create a chat endpoint for a specific configuration."""

    async def chat_endpoint(request: ChatRequest):
        """
        Handle chat requests using the {config_name} configuration.

        Args:
            request: ChatRequest containing messages and other parameters

        Returns:
            Text response or streaming response
        """
        base_url: str = 'https://openrouter.ai/api/v1'
        stream = request.stream if request.stream is not None else False

        # Convert Pydantic Message objects to dictionaries
        messages = [{"role": msg.role.value, "content": msg.content} for msg in request.messages]

        # Use the requests wrapper with configuration settings
        provider = RequestsWrapper(
            model=config.model,
            temperature=config.temperature,
            base_url=base_url,
            system_prompt=config.system_prompt)

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
    app.post(f"/{config_name}/chat/completions", name=f"{config_name}_chat_completions")(endpoint)


# @app.post("/chat/completions")
# async def chat_completions(request: ChatRequest):
#     """
#     Handle chat requests and return a text response using RequestsWrapper.

#     Args:
#         request: ChatRequest containing model, messages, and other parameters

#     Returns:
#         Text response or streaming response
#     """

#     # Eventually read this from config
#     base_url: str = 'https://openrouter.ai/api/v1'
#     model: str = 'x-ai/grok-4.1-fast'
#     temperature: float = 0.7
#     top_p: float = 1.0
#     system_prompt: str = "You are a helpful Canadian assistant. You say 'eh' a lot."
#     stream = request.stream if request.stream is not None else False

#     # Convert Pydantic Message objects to dictionaries
#     messages = [{"role": msg.role.value, "content": msg.content} for msg in request.messages]

#     # Use the requests wrapper to process the request
#     provider = RequestsWrapper(
#         model=model,
#         temperature=temperature,
#         base_url=base_url,
#         system_prompt=system_prompt)

#     if stream:
#         async def stream_generator():
#             async for chunk in provider.generate_stream(messages=messages):
#                 yield chunk.encode("utf-8") if isinstance(chunk, str) else chunk

#         return StreamingResponse(stream_generator(), media_type="text/event-stream")
#     else:
#         response_text = await provider.generate_text(messages=messages)
#         return response_text


@app.get("/")
async def root():
    """Root endpoint for health check."""
    return {"status": "ok", "message": "Universal AI Wrapper API is running (Requests Implementation)"}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/configurations")
async def list_configurations():
    """List all available configurations and their endpoints."""
    config_list = []
    for config_name, config in configurations.configurations.items():
        config_list.append({
            "name": config_name,
            "endpoint": f"/{config_name}/chat/completions",
            "model": config.model,
            "temperature": config.temperature,
            "top_p": config.top_p
        })
    return {"configurations": config_list}
