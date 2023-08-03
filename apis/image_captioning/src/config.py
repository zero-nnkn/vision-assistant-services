import os
from pathlib import Path

from pydantic import validator
from pydantic_settings import BaseSettings, SettingsConfigDict

CWD = Path(__file__)
SERVICE_ROOT = str(CWD.parent.parent)
print(SERVICE_ROOT)


class Settings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int
    CORS_ORIGINS: list[str]
    CORS_HEADERS: list[str]
    MODEL_PATH: str

    model_config = SettingsConfigDict(env_file=os.path.join(SERVICE_ROOT, ".env"))

    @validator("PORT")
    def port_is_valid(cls, value: int) -> int:
        if value < 1 or value > 65535:
            raise ValueError("Port must be an integer starting from 1 to 65535")
        return value


settings = Settings()
