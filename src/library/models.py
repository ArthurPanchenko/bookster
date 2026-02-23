from datetime import datetime

from sqlalchemy import Computed, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.functions import func

from src.core.db import Base


class BookModel(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(128))
    slug: Mapped[str] = mapped_column(
        String,
        Computed(
            "regexp_replace(lower(trim(title)), '\\s+', '-', 'g')", persisted=True
        ),
        unique=True,
        index=True,
    )
    author_id: Mapped[str] = mapped_column(String(128))

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
