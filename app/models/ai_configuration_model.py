from enum import Enum
from typing import List, Dict 
from pydantic import BaseModel, Field
from pydantic_yaml import to_yaml_str, parse_yaml_raw_as

class AIConfigurationModel(BaseModel):
    endpoint: str = Field(..., description="API Endpoint Key")
    model: str = Field(..., description="Model identifier")
    temperature: float = Field(0.7, ge=0.0, le=2.0, description="Sampling temperature")
    top_p : float = Field(1.0, ge=0.0, le=1.0, description="Top-p sampling parameter")
    system_prompt: str = Field(..., description="Default system prompt")
    # logger info

class AIConfigurations(BaseModel):
    configurations: Dict[str, AIConfigurationModel] = Field(default_factory=dict) 

if __name__ == "__main__":
    config = AIConfigurations()
    config.configurations["demo"] = AIConfigurationModel(
        endpoint="demo",
        model="x-ai/grok-4.1-fast",
        temperature=0.7,
        top_p=1.0,
        system_prompt="You are a helpful assistant."
    )
    print(to_yaml_str(config))