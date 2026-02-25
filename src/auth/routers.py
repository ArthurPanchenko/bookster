from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependecies import get_current_user
from src.auth.repository import user_repository
from src.auth.schemas import TokenReprSchema, UserCreateSchema, UserReprSchema
from src.core.db import get_db

auth_router = APIRouter()


@auth_router.post("/register", response_model=UserReprSchema)
async def create_user(
    user_data: UserCreateSchema, session: AsyncSession = Depends(get_db)
):
    user = await user_repository.create_user(user_data.model_dump(), session)
    return user


@auth_router.post("/login", response_model=TokenReprSchema)
async def login(login_info: UserCreateSchema, session: AsyncSession = Depends(get_db)):
    return await user_repository.login(login_info.model_dump(), session)


@auth_router.get("/me", response_model=UserReprSchema)
async def user_info(user=Depends(get_current_user)):
    return user
