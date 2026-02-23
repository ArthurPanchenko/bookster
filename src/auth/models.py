from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.db import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(64))
