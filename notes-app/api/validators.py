from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Note, User


async def check_unique_note_name_for_user(
    note_name: str,
    user: User,
    session: AsyncSession,
) -> None:
    user_note = await session.scalar(
        select(Note).where(
            Note.user_id == user.id,
            Note.name == note_name,
        ),
    )
    if user_note is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Заметка с названием {user_note.name} уже создана Вами.",
        )
