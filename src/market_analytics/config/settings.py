import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """
    Application configuration.

    Local:
        values come from .env

    Cloud / CI:
        values come from environment variables
    """

    def __init__(self):

        self.gcp_project_id = self._required("GCP_PROJECT_ID")

        self.finnhub_api_key = self._required("FINNHUB_API_KEY")

        self.google_credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

        self.gemini_api_key = os.getenv("GEMINI_API_KEY")

        # self.environment = os.getenv("ENVIRONMENT", "development")

        self.log_level = os.getenv("LOG_LEVEL", "INFO")

    @staticmethod
    def _required(name: str) -> str:
        value = os.getenv(name)

        if not value:
            raise RuntimeError(f"Missing required environment variable: {name}")

        return value


# module-level instance for easier and faster access
settings = Settings()


@lru_cache
def get_settings() -> Settings:
    return Settings()
