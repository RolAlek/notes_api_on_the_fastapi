from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api.router import main_router
from core import db_manager
from core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # start app
    yield
    # shutdown
    await db_manager.dispose()


main_app = FastAPI(title=settings.app_name, lifespan=lifespan)
main_app.include_router(main_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.socket.host,
        port=settings.socket.port,
        reload=settings.socket.reload,
    )
