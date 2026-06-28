from pydantic_settings import BaseSettings, SettingsConfigDict

from pydantic import Field

from typing import Literal


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    env: Literal["dev", "testing", "prod"] = Field(
        validation_alias="ENV", default="dev"
    )

    version: str = Field(default="0.0.0", validation_alias="VERSION")

    cors_origins: list[str] = Field(
        default=["http://localhost:5173"], validation_alias="CORS_ORIGINS"
    )

    name: str = Field(default="api", validation_alias="NAME")

    log_format: Literal["json", "pretty"] = Field(
        default="json", validation_alias="LOG_FORMAT"
    )

    log_level: Literal["debug", "info", "warning", "error"] = Field(
        default="info", validation_alias="LOG_LEVEL"
    )

    @property
    def effective_log_level(self) -> str:
        if self.env == "dev":
            return "debug"
        if self.env == "testing":
            return "warning"
        return self.log_level
