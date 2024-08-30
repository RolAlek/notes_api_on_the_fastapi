from fastapi import APIRouter

from api.endpoints import notes_router, user_router

main_router = APIRouter()
main_router.include_router(user_router)
main_router.include_router(notes_router)
