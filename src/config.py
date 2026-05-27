from pathlib import Path

from pydantic_settings import SettingsConfigDict, BaseSettings

class Settings(BaseSettings):
    OLLAMA_HOST: str
    OLLAMA_PORT: int
    SPREADSHEET_ID: str
    GOOGLE_CREDENTIALS: str = str(Path(__file__).parent.parent / "credentials.json")
    OLLAMA_MODEL: str = "qwen2.5:14b"

    @property
    def ollama_url(self):
        return f"http://{self.OLLAMA_HOST}:{self.OLLAMA_PORT}/api/generate"
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()