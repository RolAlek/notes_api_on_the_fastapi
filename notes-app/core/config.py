from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings



class SocketConfig(BaseModel):
    host: str = '0.0.0.0'
    port: int = 8000
    reload: bool
    pool_size: int = 30
    max_overflow: int = 10


class DBConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False


class Settings(BaseSettings):
    app_name: str
    socket: SocketConfig = SocketConfig()
    db: DBConfig


settings = Settings()
