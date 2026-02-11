from pymongo import MongoClient
from app.config import settings

MONGO_URI = settings.get_mongo_uri()
MONGO_DB = settings.MONGO_DB