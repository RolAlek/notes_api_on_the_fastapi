from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core.base import Base


class Note(Base):
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    text: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
