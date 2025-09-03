import re
from decimal import Decimal
from sqlalchemy import String, DateTime, func, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, validates

from app.db import Model

CONTAINER_REGEX = re.compile(r"^[A-Z]{3}U\d{7}$")


class User(Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Container(Model):
    __tablename__ = "containers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    container_number: Mapped[str] = mapped_column(String(11), unique=True, nullable=False, index=True)
    cost: Mapped[Decimal] = mapped_column(DECIMAL(12, 2), nullable=False, index=True)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())
