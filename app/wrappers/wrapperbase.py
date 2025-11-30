from abc import ABC, abstractmethod
from typing import List, Dict, AsyncIterator

class WrapperBase(ABC):

    @abstractmethod
    async def generate_text(self, messages: List[Dict], model: str|None,  temperature: float|None):
        pass
          
    @abstractmethod
    async def generate_stream(self, messages: List[Dict], model: str|None,  temperature: float|None) -> AsyncIterator[str]:
        pass

    @abstractmethod
    def model(self):
        pass

    @abstractmethod
    def temperature(self):
        pass

    @abstractmethod
    def base_url(self):
        pass

    @abstractmethod
    def system_prompt(self, messages: List[Dict]) -> str:
        pass

if __name__=='__main__':
    pass