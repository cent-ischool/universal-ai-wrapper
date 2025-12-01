# TODO


[x] remove pydantic AI and use simple requests...https://github.com/cent-ischool/ist256-chatapp/blob/main/app/llm/ollamallm.py
[x] works now with jupyter AI, extensions, which was the point.
[x] response needs to be json with metadata, not just text
[x] implement different configuration per endpoint
[x] implement yaml comfiguration loading
[x] generate a streaming response and json response like https://openrouter.ai/request-builder
[x] implement API key obfuscation

Working on logging - have request metadata add session and user_id
    - session_id: uuid.uuid4(), # TODO: fix this needs to be a lookup based on first prompt?
    - user_id: "TBD", # TODO: fix this needs to be passed in from caller
    - get uuid 7 working... move to python 3.14???
    - log the user request message in addition to the response message perhaps 
      add to the LoggingModel ?? user message / assistant response? 

[ ] handle session management (more 1 user response is a session)
[ ] implement trace logging
[ ] write tests