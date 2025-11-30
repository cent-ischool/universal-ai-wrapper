import asyncio
import os

from wrappers.pydantic_wrapper import PydanticAIWrapper

async def main():
    base_url: str = 'https://openrouter.ai/api/v1'
    model: str = 'x-ai/grok-4.1-fast'
    temperature: float = 0.7
    system_prompt: str = "You are a helpful Canadian assistant. You say 'eh' a lot."
    stream = True

    messages = [
        {"role": "user", "content": "I am going to visit Canada next month. Any tips? What should I do there?"}
    ]

    # use the pydantic wrapper to process the request
    provider = PydanticAIWrapper(
        model=model, 
        temperature=temperature, 
        base_url=base_url,
        system_prompt=system_prompt)
    
    if stream:
        print("Streaming response:")
        async for chunk in provider.generate_stream(messages=messages):
            print(chunk, end="", flush=True)
        print()
    else:
        response_text = await provider.generate_text(messages=messages)
        print("Response:", response_text)


if __name__ == "__main__":
    asyncio.run(main())