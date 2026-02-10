from pymongo import MongoClient
from pymongo.database import Database
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
MONGO_USER = os.getenv("MONGO_USER", "adminRoot")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "adminRoot100")
MONGO_DB = os.getenv("MONGO_DB", "survey_db")

MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}?authSource=admin"

class MongoDBConnection:
    def __init__(self):
        self.client = None
        self.db = None

        def connect(self):
            try:
                self.client =MongoClient(MONGO_URI)
                self.db = self.client[MONGO_DB]
                self.client.server_info()
                print(f"Successfully connected to MongoDb database: {MONGO_DB}")
                return self.db
            except Exception as e:
                print(f"Error connecting to MongoDB: {e}")
                raise 
        
    def close(self):
        if self.client:
            self.client.close()
            print("MongoDB connection closed.")

    def get_database(self) -> Database:
        if not self.db is None:
            self.connect()
        return self.db
    
mongo_connection = MongoDBConnection()

def get_db() -> Database:
    return mongo_connection.get_database()

def get_survey_collection():
    db = get_db()
    return db["surveys"]