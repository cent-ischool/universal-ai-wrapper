from loguru import logger
from .loggerbase import LoggerBase
from models.logging_model import LoggingModel

from pymongo.asynchronous.mongo_client import AsyncMongoClient

class MongoDbLogger(LoggerBase):

    def __init__(self, params: dict = None):
        self._connection_string = "mongodb://localhost:27017/"
        self._database = "ai_logs"
        self._collection = "logs"
        if params:
            self._connection_string = params.get("connection_string", self._connection_string)
            self._database = params.get("database", self._database)
            self._collection = params.get("collection", self._collection)
        self._db = AsyncMongoClient(self._connection_string)

    async def log(self, data: LoggingModel):
        db = self._db[self._database]
        collection = db[self._collection]
        mongo_data = data.model_dump(mode="json")
        mongo_data["_id"] = str(data.request_id)
        await collection.insert_one(mongo_data)

    def provider(self):
        return "mongodb"
    

    def database(self):
        return self._database
    
    def collection(self):
        return self._collection
    


