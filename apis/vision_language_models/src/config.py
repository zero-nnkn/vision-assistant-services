import os
from pathlib import Path
from typing import Dict, List

from pydantic_settings import BaseSettings

FILE = Path(__file__)
ROOT = str(FILE.parent.parent)


class Settings(BaseSettings):
    HOST: str
    PORT: int
    CORS_ORIGINS: List[str]
    CORS_HEADERS: List[str]
    PREDICTOR_NAME: str

    class Config:
        env_file = os.path.join(ROOT, '.env')


settings = Settings()
