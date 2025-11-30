from typing import List, Dict, AsyncIterator
import os
import asyncio
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.settings import ModelSettings
from .wrapperbase import WrapperBase


class PydanticAIWrapper(WrapperBase):
    """
    Pydantic AI provider implementation of WrapperBase.
    Uses pydantic-ai's Agent for text generation.
    """

    def __init__(self, 
                 base_url: str = 'https://openrouter.ai/api/v1',
                 model: str = 'x-ai/grok-4.1-fast', 
                 temperature: float = 0.7,
                 system_prompt: str = "You are a helpful assistant."):
        """
        Initialize the Pydantic AI provider with OpenRouter.
        
        Args:
            model: Model identifier for OpenRouter (default: 'x-ai/grok-4.1-fast')
            temperature: Temperature for generation (0.0 to 1.0)
        """
        self._model = model
        self._temperature = temperature
        self._base_url = base_url
        self._system_prompt = system_prompt

        # Get OpenRouter API key from environment
        api_key = os.getenv('OPENROUTER_API_KEY')
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable not set")
        
        self._provider = OpenAIProvider(
            base_url=self.base_url,
            api_key=api_key
        )

        self._model_settings = ModelSettings(
            temperature=self._temperature
        )

        # Configure OpenAI-compatible model for OpenRouter
        self._ai = OpenAIChatModel(
            model,
            provider=OpenAIProvider(
                base_url=base_url,
                api_key=api_key
            ),
            settings = self._model_settings
        )
        
        self._agent = Agent(model=self._ai)



    async def generate_text(self, messages: List[Dict]):
        """
        Generate text using Pydantic AI Agent.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            model: Optional model override
            temperature: Optional temperature override
            
        Returns:
            Generated text response
        """
        
        # Replace system prompt if provided
        messages = self._replace_system_prompt(messages)

        # Convert messages to prompt format
        # Pydantic AI expects a user prompt, so we'll concatenate messages
        prompt = self._format_messages(messages)
        
        # Run asynchronously
        result = await self._agent.run(prompt)

        return result.output
    

    async def generate_stream(self, messages: List[Dict]) -> AsyncIterator[str]:
        """
        Generate streaming text using Pydantic AI Agent.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            model: Optional model override
            temperature: Optional temperature override
            
        Yields:
            Text chunks as they are generated
        """

        # Replace system prompt if provided
        messages = self._replace_system_prompt(messages)

        # Convert messages to prompt format
        prompt = self._format_messages(messages)
        
        # Stream response
        async with self._agent.run_stream(prompt) as response:
            async for chunk in response.stream_text(delta=True):
                yield chunk
    

    @property
    def model(self):
        """Get the current model identifier."""
        return self._model
    
    @property
    def temperature(self):
        """Get the current temperature setting."""
        return self._temperature
    
    @property
    def base_url(self):
        """Get the current base URL."""
        return self._base_url

    @property
    def system_prompt(self):
        """Get the current system prompt."""
        return self._system_prompt

    def _format_messages(self, messages: List[Dict]) -> str:
        """
        Format messages list into a single prompt string.
        
        Args:
            messages: List of message dictionaries
            
        Returns:
            Formatted prompt string
        """
        formatted_parts = []
        for msg in messages:
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            if role == 'system':
                formatted_parts.append(f"System: {content}")
            elif role == 'assistant':
                formatted_parts.append(f"Assistant: {content}")
            else:  # user or default
                formatted_parts.append(f"User: {content}")
        
        return "\n\n".join(formatted_parts)
    
    def _replace_system_prompt(self, messages: List[Dict]) -> List[Dict]:
        """
        Replace or insert the system prompt in the messages list.
        
        Args:
            messages: List of message dictionaries

        Returns:
            Updated list of message dictionaries
        """
        for i, msg in enumerate(messages):
            if msg.get('role') == 'system':
                messages[i]['content'] = self._system_prompt
                break
        else:
            messages.insert(0, {"role": "system", "content": self._system_prompt})
        return messages


async def main():
    # Example usage with OpenRouter and Grok
    provider = PydanticAIWrapper(
        model='x-ai/grok-4.1-fast', 
        temperature=0.0, 
        base_url='https://openrouter.ai/api/v1',
        system_prompt="You are a helpful assistant.")
    
    messages = [
        {"role": "system", "content": "You are a helpful pirate assistant."},
        {"role": "user", "content": "What is the capital of France and list 10 things to do there?"}
    ]
    
    # Non-streaming example
    response = await provider.generate_text(messages)
    print("Response:", response)
    
    # Streaming example
    print("\nStreaming response:")
    async for chunk in provider.generate_stream(messages):
        print(chunk, end='', flush=True)
    print()


if __name__ == '__main__':
    asyncio.run(main())