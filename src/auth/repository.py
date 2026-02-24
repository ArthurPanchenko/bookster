from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import UserModel
from src.auth.security import get_hash, verify_hash
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
            select(UserModel).where(UserModel.username == username)
        )
        return res.scalar_one_or_none()

    async def login(self, login_data: dict, session: AsyncSession):
        user = await self.get_user_by_username(login_data["username"], session)

        if not user:
            raise NotFoundException("User", login_data["username"])

        if not verify_hash(login_data["password"], user.password):
            raise NotFoundException("User", login_data["username"])

        # access_token, refresh_token = create_jwt_tokens(user.username)
        # save_refresh_token(user, get_hash(token))


user_repository = UserRepository()
