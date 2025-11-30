from enum import Enum
from typing import List
from pydantic import BaseModel, Field

'''
Docstring for app.models.chat_request_model

'{
    "model": "gpt-5.1",
    "temperature": 0.7,
    "messages": [
      {
        "role": "developer",
        "content": "You are a helpful assistant."
      },
      {
        "role": "user",
        "content": "Hello!"
      }
    ]
  }'
'''

class Role(str, Enum):
    system = "system"
    user = "user"
    assistant = "assistant"


class Message(BaseModel):
    role: Role = Field(..., description="Role of the message sender")
    content: str = Field(..., min_length=1, description="Message text")


class ChatRequest(BaseModel):
    messages: List[Message] = Field(..., min_items=1, description="Conversation messages")
    stream: bool | None = Field(False, description="Whether to stream the response")
    # Included, but these are ignored, as they are controlled by the wrapper configuration
    model: str = Field(..., description="Model identifier")
    top_p : float | None = Field(1.0, ge=0.0, le=1.0, description="Top-p sampling parameter")
    temperature: float | None = Field(0.7, ge=0.0, le=2.0, description="Sampling temperature")
    max_tokens: int | None = Field(None, ge=1, description="Maximum tokens in the response")

