import secrets
from datetime import datetime, timedelta

import jwt
from passlib.context import CryptContext

from config import settings

hash_context = CryptContext(schemes=["bcrypt"])


def get_hash(pswd: str):
    return hash_context.encrypt(pswd)


def verify_hash(plain: str, hash: str):
    return hash_context.verify(plain, hash)


def generate_jwt_token(payload: dict, expire_time=timedelta(days=1)):
    payload["expire_at"] = str(datetime.now() + expire_time)
    print(payload)

    access_token = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

    return access_token


def generate_refresh_token():
    return secrets.token_urlsafe(32)
