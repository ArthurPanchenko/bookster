from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.repository import user_repository
from src.auth.schemas import UserReprSchema, UserCreateSchema
from src.auth.security import get_hash
from src.core.db import get_db

auth_router = APIRouter()


@auth_router.post("/register", response_model=UserReprSchema)
async def create_user(user_data: UserCreateSchema, session: AsyncSession = Depends(get_db)):
    user_data.password = get_hash(user_data.password)
    user = await user_repository.create_user(user_data.model_dump(), session)
    return user


@auth_router.get("/user/{username}", response_model=UserReprSchema)
async def user_info(username: str, session: AsyncSession = Depends(get_db)):
    user = await user_repository.get_user_by_username(username, session)
    if not user:
        raise HTTPException(status_code=404, detail="User no found")
    return user
