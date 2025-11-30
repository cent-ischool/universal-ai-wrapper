from typing import List, Dict, AsyncIterator
import os
import asyncio
import requests
import sys
import json
from pathlib import Path

# Add parent directory to path for standalone execution
if __name__ == '__main__':
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from wrappers.wrapperbase import WrapperBase
else:
    from .wrapperbase import WrapperBase


class RequestsWrapper(WrapperBase):
    """
    Requests-based implementation of WrapperBase.
    Uses standard requests library for OpenAI-compatible API calls.
    """

    def __init__(self,
                 base_url: str = 'https://openrouter.ai/api/v1',
                 model: str = 'x-ai/grok-4.1-fast',
                 temperature: float = 0.7,
                 top_p: float = 1.0,
                 stream: bool = False,
                 system_prompt: str = "You are a helpful assistant."):
        """
        Initialize the Requests wrapper with OpenRouter.

        Args:
            base_url: Base URL for the API endpoint
            model: Model identifier for OpenRouter (default: 'x-ai/grok-4.1-fast')
            temperature: Temperature for generation (0.0 to 1.0)
            system_prompt: Default system prompt
        """
        self._model = model
        self._temperature = temperature
        self._base_url = base_url
        self._system_prompt = system_prompt
        self._top_p = top_p
        self._stream = stream

        # Get OpenRouter API key from environment
        self._api_key = os.getenv('OPENROUTER_API_KEY')
        if not self._api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable not set")


    async def generate_text(self, messages: List[Dict]):
        """
        Generate text using requests library.

        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            model: Optional model override

        Returns:
            Generated text response
        """
        # Replace system prompt if provided
        messages = self._replace_system_prompt(messages)

        # Prepare request payload
        payload = {
            "model": self._model,
            "messages": messages,
            "temperature": self._temperature,
            "top_p": self._top_p,
            "stream": False 
        }
        # add optional keys 

        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json"
        }

        # Run synchronous requests call in executor to avoid blocking
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: requests.post(
                f"{self._base_url}/chat/completions",
                json=payload,
                headers=headers,
                stream=False
            )
        )

        response.raise_for_status()
        result = response.json()
        # TODO this is where logging would go
        print(result)

        return result


    async def generate_stream(self, messages: List[Dict]) -> AsyncIterator[str]:
        """
        Generate streaming text using requests library.
        Returns raw SSE format data for client processing.

        Args:
            messages: List of message dictionaries with 'role' and 'content' keys

        Yields:
            Raw SSE formatted lines (data: {...})
        """
        # Use provided parameters or fall back to instance defaults

        # Replace system prompt if provided
        messages = self._replace_system_prompt(messages)

        # Prepare request payload
        payload = {
            "model": self._model,
            "messages": messages,
            "temperature": self._temperature,
            "top_p": self._top_p,
            "stream": True
        }

        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json"
        }

        # Run streaming request in executor
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: requests.post(
                f"{self._base_url}/chat/completions",
                json=payload,
                headers=headers,
                stream=True
            )
        )

        response.raise_for_status()

        # Collect complete response for logging
        complete_response = []
        complete_data = None

        # Stream the raw response lines
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                if line_str.startswith('data: '):
                    data_str = line_str[6:]  # Remove 'data: ' prefix

                    # Handle [DONE] message
                    if data_str.strip() == '[DONE]':
                        # TODO this is where logging would go
                        # Reconstruct complete response with all metadata
                        if complete_data:
                            complete_data['choices'][0]['message'] = {
                                'role': 'assistant',
                                'content': ''.join(complete_response)
                            }
                            # Remove delta from choices since we have the full message
                            if 'delta' in complete_data['choices'][0]:
                                del complete_data['choices'][0]['delta']
                            print(complete_data)
                        # Yield the [DONE] message to client
                        yield line_str + '\n\n'
                        break

                    try:
                        import json
                        data = json.loads(data_str)

                        # Store the last complete data object for metadata
                        if complete_data is None:
                            complete_data = data

                        # Collect content for logging
                        if 'choices' in data and len(data['choices']) > 0:
                            delta = data['choices'][0].get('delta', {})
                            if 'content' in delta:
                                content_chunk = delta['content']
                                complete_response.append(content_chunk)

                        # Yield the raw SSE line to client
                        yield line_str + '\n\n'
                    except json.JSONDecodeError:
                        # Skip invalid JSON lines
                        continue


    @property
    def model(self):
        """Get the current model identifier."""
        return self._model

    @property
    def temperature(self):
        """Get the current temperature setting."""
        return self._temperature

    @property
    def top_p(self):
        """Get the current top_p setting."""
        return self._top_p

    @property
    def base_url(self):
        """Get the current base URL."""
        return self._base_url

    @property
    def system_prompt(self):
        """Get the current system prompt."""
        return self._system_prompt

    def _replace_system_prompt(self, messages: List[Dict]) -> List[Dict]:
        """
        Replace or insert the system prompt in the messages list.

        Args:
            messages: List of message dictionaries

        Returns:
            Updated list of message dictionaries
        """
        # Create a copy to avoid mutating the original
        messages = messages.copy()

        for i, msg in enumerate(messages):
            if msg.get('role') == 'system':
                messages[i] = {**msg, 'content': self._system_prompt}
                return messages

        # If no system message found, insert at the beginning
        messages.insert(0, {"role": "system", "content": self._system_prompt})
        return messages


async def main():
    # Check if API key is available
    if not os.getenv('OPENROUTER_API_KEY'):
        print("OPENROUTER_API_KEY not set. Skipping live API test.")
        print("RequestsWrapper class loaded successfully!")
        print("\nTo test with real API calls, set the OPENROUTER_API_KEY environment variable.")
        return

    # Example usage with OpenRouter and Grok
    provider = RequestsWrapper(
        model='x-ai/grok-4.1-fast',
        temperature=0.0,
        top_p=1.0,
        base_url='https://openrouter.ai/api/v1',
        system_prompt="You are a helpful assistant.")

    messages = [
        {"role": "system", "content": "You are a helpful pirate assistant."},
        {"role": "user", "content": "What is the capital of France and list 10 things to do there?"}
    ]

    # Non-streaming example
    print("Non-streaming response:")
    response = await provider.generate_text(messages)
    print("Response:", response)

    # Streaming example
    print("\n\nStreaming response:")
    async for chunk in provider.generate_stream(messages):
        print(chunk, end='', flush=True)
    print()


if __name__ == '__main__':
    asyncio.run(main())
