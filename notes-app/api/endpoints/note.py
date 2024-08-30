from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.validators import check_unique_note_name_for_user
from core import check_spelling, db_manager
from core.user import current_user
from crud import notes_crud
from models import Note, User
from schemas import NoteCreate, NoteRead

router = APIRouter(prefix="/notes", tags=["Notes"])


@router.post("/", status_code=HTTPStatus.CREATED, response_model=NoteRead)
async def create_note(
    new_note: NoteCreate,
    session: AsyncSession = Depends(db_manager.get_session),
    user: User = Depends(current_user),
) -> Note:
    await check_unique_note_name_for_user(new_note.name, user, session)
    corrected_name, corrected_text = await check_spelling(
        [
            new_note.name,
            new_note.text,
        ],
    )
    return await notes_crud.create(
        NoteCreate(name=corrected_name, text=corrected_text),
        session,
        user,
    )


@router.get(
    "/my",
    response_model=list[NoteRead],
    dependencies=[Depends(current_user)],
)
async def get_all_user_notes(
    session: AsyncSession = Depends(db_manager.get_session),
    user: User = Depends(current_user),
) -> list[Note]:
    return await notes_crud.get_all(session, user)
