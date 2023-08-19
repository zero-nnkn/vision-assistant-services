from pathlib import Path

from pydantic_settings import BaseSettings

FILE = Path(__file__)
ROOT = FILE.parent.parent


class Settings(BaseSettings):
    # PROJECT INFORMATION
    # HOST: str
    # PORT: int
    CORS_ORIGINS: list
    CORS_HEADERS: list

    # ML INFORMATION
    FASTER_WHISPER_MODEL: str
    FASTER_WHISPER_MODEL_DEVICE: str
    FASTER_WHISPER_MODEL_COMPUTE_TYPE: str

    class Config:
        env_file = ROOT / '.env'


settings = Settings()
