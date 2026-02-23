from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import UserModel


class UserRepository:

    async def create_user(self, user_data: dict, session: AsyncSession):
        user = UserModel(**user_data)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    async def get_user_by_username(self, username: str, session: AsyncSession):
        res = await session.execute(select(UserModel).where(UserModel.username == username))
        return res.scalar_one_or_none()
        

user_repository = UserRepository()
