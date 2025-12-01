from enum import Enum
from typing import List, Dict 
from pydantic import BaseModel, Field
from pydantic_yaml import to_yaml_str, parse_yaml_raw_as

class AIConfigurationModel(BaseModel):
    api_key: str = Field(..., description="API key for the AI service")
    endpoint: str = Field(description="API endpoint URL", default="")
    model: str = Field(..., description="Model identifier")
    description: str = Field(..., description="Description of the AI configuration")
    temperature: float = Field(0.7, ge=0.0, le=2.0, description="Sampling temperature")
    top_p : float = Field(1.0, ge=0.0, le=1.0, description="Top-p sampling parameter")
    system_prompt: str = Field(..., description="Default system prompt")
    logger_type: str = Field(default="console", description="Logger type to be used")
    logger_params: Dict[str, str] = Field(default_factory=dict, description="Parameters for the logger")
    # logger info

class AIConfigurationReportingModel(BaseModel):
    endpoint: str = Field(..., description="API endpoint used for the request")
    model: str = Field(..., description="Model identifier")
    temperature: float = Field(..., description="Sampling temperature")
    top_p : float = Field(..., description="Top-p sampling parameter")
    system_prompt: str = Field(..., description="Default system prompt")

class AIConfigurations(BaseModel):
    configurations: Dict[str, AIConfigurationModel] = Field(default_factory=dict) 

if __name__ == "__main__":
    with open("app/config.yaml", "r") as f:
        yaml_content = f.read()
    config = parse_yaml_raw_as(AIConfigurations, yaml_content)
    print(to_yaml_str(config))