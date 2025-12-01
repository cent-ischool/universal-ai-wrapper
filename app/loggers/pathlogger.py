from pathlib import Path
from .loggerbase import LoggerBase
from app.models.logging_model import LoggingModel

class PathJsonFileLogger(LoggerBase):

    def __init__(self, params: dict = None):
        self._path = "somefolder"
        if params:
            self._path = params.get("path", self._path)

        folder_path = Path(self._path)
        folder_path.mkdir(exist_ok=True)


    async def log(self, data: LoggingModel):
        filename = f"{data.request_id}.json"
        full_path = Path(self._path) / filename
        with open(full_path, "w") as log_file:
            log_file.write(data.model_dump_json())

    def provider(self):
        return "path"
    

    def path(self):
        return self._path
    


