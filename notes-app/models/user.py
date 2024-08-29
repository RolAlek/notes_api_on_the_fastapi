from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy.orm import Mapped, relationship

from core.db import Base

if TYPE_CHECKING:
    from .note import Note


class User(SQLAlchemyBaseUserTable[int], Base):
    notes: Mapped[list["Note"]] = relationship(back_populates="user")
