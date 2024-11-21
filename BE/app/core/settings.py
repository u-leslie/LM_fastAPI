from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "mysecretkey" 
    ALGORITHM: str = "HS256" 
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  

    class Config:
        env_file = ".env"  # Points to the .env file to load environment variables
