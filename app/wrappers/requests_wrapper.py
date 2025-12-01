from typing import List, Dict, AsyncIterator
import os
import asyncio
import requests
import sys
import json
from pathlib import Path
import uuid
import datetime

from app.loggers.loggerfactory import LoggerFactory
from app.models.logging_model import LoggingModel
from app.models.ai_configuration_model import AIConfigurationModel
from app.wrappers.wrapperbase import WrapperBase

def unix_to_iso8601(timestamp):
  """Converts a Unix timestamp to an ISO 8601 formatted string."""
  # Convert the Unix timestamp to a datetime object in UTC
  dt_object = datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)
  # Format the datetime object to ISO 8601 string
  iso_string = dt_object.isoformat()
  return iso_string

def build_log_entry(result: Dict, config: AIConfigurationModel, messages: List[Dict]) -> LoggingModel:
    log_entry = LoggingModel(
        request_id= uuid.uuid4(),
        provider=result.get("provider", "unknown"),
        model=config.model,
        endpoint=config.endpoint,
        session_id= uuid.uuid4(), # TODO: fix this needs to be a lookup based on first prompt?
        user_id="TBD", # TODO: fix this needs to be passed in from caller
        timestamp=unix_to_iso8601(result.get("created", datetime.datetime.now().timestamp())),
        role=result['choices'][0]['message'].get('role', 'assistant'),
        message=result['choices'][0]['message'].get('content', '')
        # usage =result.get("usage", {}),
        # ai_configuration= config,
        # input_messages=messages
    )
    return log_entry


class RequestsWrapper(WrapperBase):
    """
    Requests-based implementation of WrapperBase.
    Uses standard requests library for OpenAI-compatible API calls.
    """

    def __init__(self,
                 config: AIConfigurationModel,
                 base_url: str = 'https://openrouter.ai/api/v1'):
        """
        Initialize the Requests wrapper with OpenRouter.

        Args:
            base_url: Base URL for the API endpoint
            model: Model identifier for OpenRouter (default: 'x-ai/grok-4.1-fast')
            temperature: Temperature for generation (0.0 to 1.0)
            system_prompt: Default system prompt
        """
        self._base_url = base_url
        self._config = config
        self._logger = LoggerFactory.create(
            config.logger_type,
            config.logger_params
        )

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
            "model": self._config.model,
            "messages": messages,
            "temperature": self._config.temperature,
            "top_p": self._config.top_p,
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

        # Log the complete response
        log_data = build_log_entry(result, self._config, messages)        
        await self._logger.log(log_data)

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
            "model": self._config.model,
            "messages": messages,
            "temperature": self._config.temperature,
            "top_p": self._config.top_p,
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

                            # Log the data 
                            log_data = build_log_entry(complete_data, self._config, messages)
                            await self._logger.log(log_data)
                            
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
    def config(self) -> AIConfigurationModel:
        """Get the current configuration."""
        return self._config


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
                messages[i] = {**msg, 'content': self._config.system_prompt}
                return messages

        # If no system message found, insert at the beginning
        messages.insert(0, {"role": "system", "content": self._config.system_prompt})
        return messages

