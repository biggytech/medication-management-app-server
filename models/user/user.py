from dataclasses import dataclass

from sqlalchemy import Boolean
from sqlalchemy import Date
from sqlalchemy import String
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from models.base import Base
from models.common.enums.sex_types import SexTypesType


@dataclass
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(UUID(as_uuid=True), unique=True, server_default=text("gen_random_uuid()"))
    full_name: Mapped[str] = mapped_column(String(255))
    is_guest: Mapped[bool] = mapped_column(Boolean())
    password: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255))  # TODO: make unique
    sex: Mapped[str] = mapped_column(SexTypesType, nullable=True)  # Optional field for sex
    date_of_birth: Mapped[Date] = mapped_column(Date, nullable=True)  # Optional field for date of birth

    # addresses: Mapped[List["Address"]] = relationship(
    #     back_populates="user", cascade="all, delete-orphan"
    # )
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, full_name={self.full_name!r}, is_guest={self.is_guest!r}, email={self.email!r})"

    def as_dict(self):
        from services.user.get_is_doctor import get_is_doctor
        user_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        user_dict['is_doctor'] = get_is_doctor(user_dict['id'])
        return user_dict
