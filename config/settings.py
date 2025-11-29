import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # API Keys
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

    # Agent URLs
    HR_AGENT_URL = os.getenv("HR_AGENT_URL", "http://localhost:8001")
    IT_AGENT_URL = os.getenv("IT_AGENT_URL", "http://localhost:8002")

    # Model Configuration
    DEFAULT_MODEL = "gemini-2.0-flash-exp"

    # Database
    DB_PATH = "./data/onboarding_sessions.db"

    # Logging
    LOG_LEVEL = "INFO"


settings = Settings()
