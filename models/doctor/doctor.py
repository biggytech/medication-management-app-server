from dataclasses import dataclass

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base
from models.user.user import User


@dataclass
class Doctor(Base):
    """
    Doctor model to track doctor users.
    Each doctor is linked to a user account and has additional professional information.
    """
    __tablename__ = "doctors"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    specialisation: Mapped[str] = mapped_column(String(255), nullable=False)
    place_of_work: Mapped[str] = mapped_column(String(255), nullable=False)
    photo_url: Mapped[str] = mapped_column(String(500), nullable=True)  # Local file path for photo

    # Relationship to User model
    user: Mapped["User"] = relationship("User")

    def __repr__(self) -> str:
        return f"Doctor(id={self.id!r}, user_id={self.user_id!r}, specialisation={self.specialisation!r}, place_of_work={self.place_of_work!r})"
