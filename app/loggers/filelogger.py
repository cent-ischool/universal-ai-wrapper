from loguru import logger
from .loggerbase import LoggerBase
from models.logging_model import LoggingModel

class LineOrientedJsonFileLogger(LoggerBase):

    def __init__(self, params: dict = None):
        self._filespec = "applog.json"
        if params:
            self._filespec = params.get("filespec", self._filespec)

    async def log(self, data: LoggingModel):
        with open(self._filespec, "a") as log_file:
            log_file.write(data.model_dump_json() + "\n")

    def provider(self):
        return "jsonfile"
    

    def filespec(self):
        """Get the current log file specification."""
        return self._filespec
    


