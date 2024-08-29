from .base import CRUDManager
from models import Note


notes_crud = CRUDManager(Note)
