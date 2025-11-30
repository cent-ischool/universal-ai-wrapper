from fastapi import FastAPI
from app.models.chat_request_model import ChatRequest
from app.models.chat_response_model import WrapperResponse
from app.wrappers.pydantic_wrapper import PydanticAIWrapper
import time
import uuid
from fastapi.responses import StreamingResponse

app = FastAPI(title="Universal AI Wrapper API")


@app.post("/chat/default")
async def chat_default(request: ChatRequest):
    """
    Handle chat requests and return a text response.
    
    Args:
        request: ChatRequest containing model, messages, and other parameters
        
    Returns:
        Text response or streaming response
    """

    # Eventually read this from config
    base_url: str = 'https://openrouter.ai/api/v1'
    model: str = 'x-ai/grok-4.1-fast'
    temperature: float = 0.7
    system_prompt: str = "You are a helpful Canadian assistant. You say 'eh' a lot."
    stream = request.stream if request.stream is not None else False

    # Convert Pydantic Message objects to dictionaries
    messages = [{"role": msg.role.value, "content": msg.content} for msg in request.messages]

    # use the pydantic wrapper to process the request
    provider = PydanticAIWrapper(
        model=model,
        temperature=temperature,
        base_url=base_url,
        system_prompt=system_prompt)
    
    if stream:
        async def stream_generator():
            async for chunk in provider.generate_stream(messages=messages):
                # Ensure bytes are yielded
                if isinstance(chunk, bytes):
                    yield chunk
                else:
                    yield chunk.encode("utf-8")

        return StreamingResponse(stream_generator(), media_type="text/plain")
    else:
        response_text = await provider.generate_text(messages=messages)
        return response_text



    # # Create a sample response
    # response = WrapperResponse(
    #     user_id="sample_user_123",
    #     timestamp=int(time.time()),
    #     session_id=uuid.uuid4()
    # )
    
    # return response


@app.get("/")
async def root():
    """Root endpoint for health check."""
    return {"status": "ok", "message": "Universal AI Wrapper API is running"}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}