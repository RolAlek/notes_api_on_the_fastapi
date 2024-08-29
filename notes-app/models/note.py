from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base

if TYPE_CHECKING:
    from .user import User


class Note(Base):
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    text: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    create_date: Mapped[datetime] = mapped_column(default=datetime.now)
    user: Mapped['User'] = relationship(back_populates='notes')
