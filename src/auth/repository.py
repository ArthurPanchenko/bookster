from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.auth.models import RefreshTokenModel, UserModel
from src.auth.security import (
    generate_jwt_token,
    generate_refresh_token,
    get_hash,
    verify_hash,
)
from src.core.exceptions import NotFoundException


class UserRepository:
    async def create_user(self, user_data: dict, session: AsyncSession):
        user_data["password"] = get_hash(user_data["password"])
        user = UserModel(**user_data)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    async def get_user_by_username(self, username: str, session: AsyncSession):
        res = await session.execute(
            select(UserModel)
            .where(UserModel.username == username)
            .options(selectinload(UserModel.refresh_token))
        )
        return res.scalar_one_or_none()

    async def create_refresh_token(
        self, token: str, user_id: int, session: AsyncSession
    ):

        token = RefreshTokenModel(token=token, user_id=user_id)
        session.add(token)
        await session.commit()
        await session.refresh(token)
        return token

    async def login(self, login_data: dict, session: AsyncSession):
        user = await self.get_user_by_username(login_data["username"], session)

        if not user:
            raise NotFoundException("User", login_data["username"])
        if not verify_hash(login_data["password"], user.password):
            raise NotFoundException(
                "User", login_data["username"]
            )  # Exception - bad credentials
        if user.refresh_token:
            raise NotFoundException(
                "User", login_data["username"]
            )  # Exception - already loged in

        access_token = generate_jwt_token({"username": user.username})

        refresh_token = generate_refresh_token()
        await self.create_refresh_token(get_hash(refresh_token), user.id, session)

        return {"access_token": access_token, "refresh_token": refresh_token}


user_repository = UserRepository()
