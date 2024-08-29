from typing import Generic, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import Base
from models import User

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)


class CRUDManager(Generic[ModelType, CreateSchemaType]):
    def __init__(self, model: Type[ModelType]) -> None:
        self.model = model

    async def create(
        self,
        data_in: CreateSchemaType,
        session: AsyncSession,
        user: User,
    ) -> ModelType:
        new_data = data_in.model_dump()
        new_data["user_id"] = user.id
        db_obj = self.model(**new_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
