import os
from dotenv import load_dotenv

load_dotenv()
class Settings:
    """
        Reads values from environment variables with optional defaults.
    """
    # Database url
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    # Used by JWT for encoding and decoding
    SECRET_KEY: str = os.getenv("SECRET_KEY", "defaultsecret")

settings = Settings()
