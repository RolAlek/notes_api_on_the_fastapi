from typing import Any, AsyncGenerator

from fastapi import Depends, Request
from fastapi_users import (
    BaseUserManager,
    FastAPIUsers,
    IntegerIDMixin,
    InvalidPasswordException,
)
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from schemas import UserCreate

from . import db_manager
from .config import settings


async def get_user_db(
    session: AsyncSession = Depends(db_manager.get_session),
) -> AsyncGenerator[SQLAlchemyUserDatabase[User, Any], None]:
    yield SQLAlchemyUserDatabase(session, User)


bearer_transport = BearerTransport(tokenUrl="/api/auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.secret, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    async def validate_password(
        self,
        password: str,
        user: UserCreate | User,
    ) -> None:
        if len(password) < 8:
            raise InvalidPasswordException(
                reason="Пароль должен иметь длину от 8 символов",
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason="Пароль не должен содержать e-mail",
            )

    async def on_after_register(
        self,
        user: User,
        request: Request | None = None,
    ) -> None:
        print(f"Пользователь {user.email} успешно создан!")


async def get_user_manager(
    user_db=Depends(get_user_db),
) -> AsyncGenerator[UserManager, None]:
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)
current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
