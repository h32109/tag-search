import os
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict

from searcher.enums import Environment
from searcher.utils import get_path_from_root


class Setting(BaseSettings):
    APP_VERSION: str = "0.0.1"
    ENV: Environment = Environment.DEV

    UVICORN_HOST: str = "0.0.0.0"
    UVICORN_PORT: int = 8000

    LOGGING_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    SQL_URL: str
    SQL_DATABASE: str

    @property
    def is_dev(self) -> bool:
        return self.ENV == Environment.DEV

    model_config = SettingsConfigDict(
        env_file=get_path_from_root(f'config/{os.getenv("PROFILE", "dev")}.env'),
        env_file_encoding='utf-8',
        case_sensitive=False
    )


settings = Setting()
