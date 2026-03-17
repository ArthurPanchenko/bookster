from pydantic import BaseModel


class UserCreateSchema(BaseModel):
    username: str
    password: str


class UserReprSchema(BaseModel):
    model_config = {"from_attributes": True}
    username: str


class TokenReprSchema(BaseModel):
    access_token: str
    refresh_token: str | None = None
