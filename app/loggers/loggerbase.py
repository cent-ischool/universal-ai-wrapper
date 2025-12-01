from abc import ABC, abstractmethod
from typing import List, Dict, AsyncIterator
from app.models.logging_model import LoggingModel

class LoggerBase(ABC):

    @abstractmethod
    async def log(self, data: LoggingModel):
        pass

    @abstractmethod
    def provider(self):
        pass

if __name__=='__main__':
    pass