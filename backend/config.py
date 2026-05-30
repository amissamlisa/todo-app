import os
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    JWT_SECRET_KEY: str = os.environ["JWT_SECRET_KEY"]
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    PASSWORD_RESET_TOKEN_EXPIRE_HOURS: int = 1
    PASSWORD_RESET_URL: str = os.environ["PASSWORD_RESET_URL"]
    RESEND_API_KEY: str = os.environ["RESEND_API_KEY"]
    ALLOWED_ORIGIN_URL: str = os.environ["ALLOWED_ORIGIN_URL"]
    COOKIE_SECURE: bool = os.getenv("COOKIE_SECURE", "false").lower() == "true"
    OPENAI_API_KEY: str = os.environ["OPENAI_API_KEY"]
    OPENAI_TIMEOUT_SECONDS: float = float(os.getenv("OPENAI_TIMEOUT_SECONDS", "600"))
settings = Settings()
