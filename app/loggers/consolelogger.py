from .loggerbase import LoggerBase
from models.logging_model import LoggingModel

class ConsoleLogger(LoggerBase):

    async def log(self, data: LoggingModel):
        print("Logging Data:")
        print(data.model_dump_json())

    def provider(self):
        return "ConsoleLogger"