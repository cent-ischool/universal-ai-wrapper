from enum import Enum
from typing import List, Dict 
from pydantic import BaseModel, Field
import uuid 
from app.models.chat_request_model import Role, Message
from app.models.ai_configuration_model import AIConfigurationReportingModel


class AIUsage(BaseModel):
    prompt_tokens: int = Field(..., description="Number of tokens in the prompt")
    completion_tokens: int = Field(..., description="Number of tokens in the completion")
    total_tokens: int = Field(..., description="Total number of tokens used")

class LoggingModel(BaseModel):
    #base fields
    request_id: uuid.UUID = Field(default_factory=uuid.uuid4, description="Unique identifier for the request")
    provider: str = Field(..., description="AI service provider name")
    model: str = Field(..., description="Model identifier")
    endpoint: str = Field(..., description="API endpoint used for the request")
    session_id: uuid.UUID = Field(default_factory=uuid.uuid4, description="Session identifier for grouping related requests")
    user_id: str = Field(..., description="Identifier for the user making the request")
    timestamp: str = Field(..., description="Timestamp of the request")
    role: Role = Field(..., description="Role of the user making the request")
    message: str = Field(..., description="Message content sent to the AI service")

    # composite fields
    # usage: AIUsage = Field(..., description="Usage statistics for the AI service")
    # ai_configuration: AIConfigurationReportingModel = Field(..., description="AI configuration settings")
    # input_messages: List[Message] = Field(..., description="List of input messages sent to the AI service")
