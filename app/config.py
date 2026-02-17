from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    
    MONGO_HOST: str = Field(default="localhost")
    MONGO_PORT: int = Field(default=27017)
    MONGO_USER: str = Field(default="adminRoot")
    MONGO_PASSWORD: str = Field(default="adminRoot100")
    MONGO_DB: str = Field(default="survey_db")
    
    APP_HOST: str = Field(default="0.0.0.0")
    APP_PORT: int = Field(default=8000)
    #use AWS S3 -> setup an account for it
    UPLOAD_DIR: str = Field(default="uploads")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
    
    def get_mongo_uri(self) -> str:
        return f"mongodb://{self.MONGO_USER}:{self.MONGO_PASSWORD}@{self.MONGO_HOST}:{self.MONGO_PORT}/"

settings = Settings()