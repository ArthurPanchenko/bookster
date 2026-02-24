from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(64))

    refresh_token: Mapped["RefreshTokenModel"] = relationship(
        back_populates="user", uselist=False, cascade="all, delete-orphan"
    )


class RefreshTokenModel(Base):
    __tablename__ = "tokens"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    token: Mapped[str] = mapped_column(String(255))
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), index=True, unique=True
    )

    user: Mapped[UserModel] = relationship(back_populates="refresh_token")
