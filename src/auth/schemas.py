from pydantic import BaseModel


class UserCreateSchema(BaseModel):
    username: str
    password: str


class UserReprSchema(BaseModel):
    username: str


class TokenReprSchema(BaseModel):
    access_token: str
    refresh_token: str | None = None
