from pydantic import BaseModel


class UserCreateSchema(BaseModel):
    username: str
    password: str
    
class UserReprSchema(BaseModel):
    username: str