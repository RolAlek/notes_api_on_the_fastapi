import uvicorn
from api import router as main_router
from core.config import settings
from fastapi import FastAPI

app = FastAPI(title=settings.app_name)
app.include_router(main_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.socket.host,
        port=settings.socket.port,
        reload=True,
    )
