from loguru import logger
from .loggerbase import LoggerBase
from app.models.logging_model import LoggingModel

class LoguruLogger(LoggerBase):

    def __init__(self, params: dict = None):
        if params:
            logger.add(params["target"], level=params.get("level", "INFO"))
        

    async def log(self, data: LoggingModel):
        logger.info("Logging Data:")
        logger.info(data.model_dump_json())

    def provider(self):
        return "loguru"
    

