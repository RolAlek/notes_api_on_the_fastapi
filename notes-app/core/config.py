from pydantic import BaseModel
from pydantic_settings import BaseSettings


class SocketConfig(BaseModel):
    host: str = '0.0.0.0'
    port: int = 8000
    reload: bool


class Settings(BaseSettings):
    app_name: str
    socket: SocketConfig = SocketConfig()
    


settings = Settings()
