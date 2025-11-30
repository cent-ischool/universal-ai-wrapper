from enum import Enum
from typing import List, Dict 
from pydantic import BaseModel, Field
from pydantic_yaml import to_yaml_str, parse_yaml_raw_as

class AIConfigurationModel(BaseModel):
    model: str = Field(..., description="Model identifier")
    description: str = Field(..., description="Description of the AI configuration")
    temperature: float = Field(0.7, ge=0.0, le=2.0, description="Sampling temperature")
    top_p : float = Field(1.0, ge=0.0, le=1.0, description="Top-p sampling parameter")
    system_prompt: str = Field(..., description="Default system prompt")
    # logger info

class AIConfigurations(BaseModel):
    configurations: Dict[str, AIConfigurationModel] = Field(default_factory=dict) 

if __name__ == "__main__":
    with open("app/config.yaml", "r") as f:
        yaml_content = f.read()
    config = parse_yaml_raw_as(AIConfigurations, yaml_content)
    print(to_yaml_str(config))