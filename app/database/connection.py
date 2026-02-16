from pymongo import MongoClient
from app.config import settings

class MongoDBConnection:
    _client = None
    _db = None

    @classmethod
    def connect(cls):
        if cls._client is None:
            mongo_uri = settings.get_mongo_uri()
            cls._client = MongoClient(mongo_uri)
            cls._db = cls._client[settings.MONGO_DB]
            print(f"Connected to MongoDB: {settings.MONGO_DB}")

    @classmethod
    def close(cls):
        if cls._client:
            cls._client.close()
            cls._client = None
            cls._db = None
            print("MongoDB connection closed")

    @classmethod
    def get_database(cls):
        if cls._db is None:
            cls.connect()
        return cls._db

def get_db():
    return MongoDBConnection.get_database()

def get_survey_collection():
    db = get_db()
    return db["surveys"]