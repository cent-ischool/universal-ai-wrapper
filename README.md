# Universal AI Wrapper

The Universal AI Wrapper is a web API that provides a unified interface to interact with various AI models and services. It offers the following advantages over using individual AI services directly:

1. API key and access key obfuscation: The wrapper hides sensitive keys from the client, enhancing security.
2. Additional metadata: The wrapper can add useful metadata to requests and responses, improving traceability and context.
3. Logging: The wrapper can log requests and responses for monitoring and debugging purposes.
4. You can create multiple endpoints and 


## YAML configuration

The Universal AI Wrapper is configured using a YAML file. Below is an example configuration:

```yaml

demo:
  system_prompt: "You are a helpful assistant."
  endpoint: demo
  temperature: 0.7
  model: gpt-4o-mini
  

  endpoint: demo
  api_key: 
  provider: openai
    model: gpt-4o-mini
  logger:
    type: file

```


Examples

```bash
curl -X POST "http://localhost:8000/chat/default" \
     -H "Content-Type: application/json" \
     -d '{
  "model": "any",
  "messages": [
    {
      "role": "user",
      "content": "why did the chicken cross the road?"
    }
  ],
  "top_p": 1,
  "temperature": 0.7,
  "max_tokens": 1,
  "stream": true
}'
```