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

    # AWS S3 Configuration
    AWS_ACCESS_KEY_ID: str = Field(default="")
    AWS_SECRET_ACCESS_KEY: str = Field(default="")
    AWS_REGION: str = Field(default="us-east-1") # Example region, change as needed
    S3_BUCKET_NAME: str = Field(default="your-s3-bucket-name") # Replace with your S3 bucket name

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
    
    def get_mongo_uri(self) -> str:
        return f"mongodb://{self.MONGO_USER}:{self.MONGO_PASSWORD}@{self.MONGO_HOST}:{self.MONGO_PORT}/"

settings = Settings()