
from .loggerbase import LoggerBase

class LoggerFactory:

    @staticmethod
    def create(logger_type: str, params: dict = None) -> LoggerBase:
        if logger_type == "console":
            from .consolelogger import ConsoleLogger
            return ConsoleLogger(params)
        
        if logger_type == "loguru":
            from .logurulogger import LoguruLogger
            return LoguruLogger(params)
        
        if logger_type == "jsonfile":
            from .filelogger import LineOrientedJsonFileLogger
            return LineOrientedJsonFileLogger(params)
        
        if logger_type == "mongodb":
            from .mongodblogger import MongoDbLogger
            return MongoDbLogger(params)

        raise ValueError(f"Unknown logger type: {logger_type}")
    

