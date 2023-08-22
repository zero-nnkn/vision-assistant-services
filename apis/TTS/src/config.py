import os
from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings

FILE = Path(__file__)
ROOT = str(FILE.parent.parent)


class Settings(BaseSettings):
    # PROJECT INFORMATION
    HOST: str
    PORT: int
    CORS_ORIGINS: List[str]
    CORS_HEADERS: List[str]

    # ML INFORMATION
    MODEL_NAME: str
    MODEL_PATH: str
    CONFIG_PATH: str
    VOCODER_PATH: str
    VOCODER_CONFIG_PATH: str
    MODEL_DEVICE: str

    class Config:
        env_file = os.path.join(ROOT, ".env")


settings = Settings()
