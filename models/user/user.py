from sqlalchemy import text
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import UUID
from models.base import Base

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    uuid = mapped_column(UUID(as_uuid=True), unique=True, server_default=text("gen_random_uuid()"))
    full_name: Mapped[str] = mapped_column(String(255))
    is_guest: Mapped[bool] = mapped_column(Boolean())
    password: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255)) # TODO: make unique
    # addresses: Mapped[List["Address"]] = relationship(
    #     back_populates="user", cascade="all, delete-orphan"
    # )
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, full_name={self.full_name!r}, is_guest={self.is_guest!r}, email={self.email!r})"
