from dataclasses import dataclass
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base
from models.user.user import User
from models.doctor.doctor import Doctor


@dataclass
class Patient(Base):
    """
    Patient model to track the relationship between users and doctors.
    This represents a many-to-many relationship where:
    - A doctor can have many patients
    - A patient (user) can have many doctors
    """
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    doctor_id: Mapped[int] = mapped_column(ForeignKey("doctors.id"))

    # Relationships
    user: Mapped["User"] = relationship("User")
    doctor: Mapped["Doctor"] = relationship("Doctor")

    def __repr__(self) -> str:
        return f"Patient(id={self.id!r}, user_id={self.user_id!r}, doctor_id={self.doctor_id!r})"
