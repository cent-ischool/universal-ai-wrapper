import sys
import os
import asyncio
from loggers.loggerfactory import LoggerFactory
from models.logging_model import LoggingModel, AIUsage
from models.ai_configuration_model import AIConfigurationReportingModel
from models.chat_request_model import Role, Message
from  dotenv import load_dotenv


async def main():
    import datetime
    load_dotenv()
    params = { "filespec": "foofilelog.json" }
    path_params = { "path": "logs" }
    mongo_params = {
        "connection_string": os.environ.get("MONGO_CONNECTION_STRING"),
        "database": "testing",
        "collection": "logs"
    }
    logger = LoggerFactory.create("path", path_params)
    print(f"Created logger of type: {logger.provider()}")

    # Create a sample LoggingModel instance
    sample_log = LoggingModel(
        provider="openrouter",
        model="gpt-4",
        endpoint="/chat/completions",
        user_id="test-user",
        timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        role=Role.user,
        message="This is a test log message.",
        usage=AIUsage(prompt_tokens=10, completion_tokens=20, total_tokens=30),
        ai_configuration=AIConfigurationReportingModel(
            endpoint="/chat/completions",
            model="gpt-4",
            temperature=0.7,
            top_p=1.0,
            system_prompt="You are a helpful assistant."
        ),
        input_messages=[Message(role=Role.user, content="Hello")]
    )

    await logger.log(sample_log)


if __name__ == '__main__':
    asyncio.run(main())
    