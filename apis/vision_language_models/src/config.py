import os
from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings

FILE = Path(__file__)
ROOT = str(FILE.parent.parent)


class Settings(BaseSettings):
    HOST: str
    PORT: int
    CORS_ORIGINS: List[str]
    CORS_HEADERS: List[str]

    S3_BUCKET_NAME: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str

    DEVICE: str
    PREDICTOR_NAME: str
    PREDICTOR_ARGS: str

    class Config:
        env_file = os.path.join(ROOT, ".env")


settings = Settings()
