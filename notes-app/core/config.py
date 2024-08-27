from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class SocketConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    pool_size: int = 30
    max_overflow: int = 10


class DBConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP__",
        env_file='../.env',
        extra='allow',
    )
    app_name: str
    secret: str
    socket: SocketConfig = SocketConfig()
    db: DBConfig


settings = Settings()
