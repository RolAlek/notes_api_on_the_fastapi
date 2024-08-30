__all__ = ["user_router", "notes_router"]

from .note import router as notes_router
from .user import router as user_router
