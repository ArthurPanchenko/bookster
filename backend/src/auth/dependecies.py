from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.repository import user_repository
from src.auth.security import decode_jwt
from src.core.db import get_db

bearer = HTTPBearer(auto_error=False)


async def get_current_user(
    creds: HTTPAuthorizationCredentials | None = Depends(bearer),
    session: AsyncSession = Depends(get_db),
):
    if creds is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No auth")

    token = creds.credentials
    decoded = decode_jwt(token)

    username = decoded["username"]
    # expire_at = decoded["expire_at"]

    user = await user_repository.get_user_by_username(username, session)

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No auth")
    return user
