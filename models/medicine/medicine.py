import datetime
import enum
from dataclasses import dataclass

from sqlalchemy import String, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import ENUM as pgEnum
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from models.base import Base
from models.medicine_schedule.medicine_schedule import MedicineSchedule


class MedicineForms(str, enum.Enum):
    tablet = "tablet"
    injection = "injection"
    solution = "solution"
    drops = "drops"
    inhaler = "inhaler"
    powder = "powder"
    other = "other"


MedicineFormsType: pgEnum = pgEnum(
    MedicineForms,
    name="medicine_forms",
    create_constraint=True,
    metadata=Base.metadata,
    validate_strings=True,
)


@dataclass
class Medicine(Base):
    __tablename__ = "medicines"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    form: Mapped[str] = mapped_column(MedicineFormsType, nullable=False)
    schedule: Mapped["MedicineSchedule"] = relationship()
    notes: Mapped[str] = mapped_column(String(255), nullable=True)
    deleted_date: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    count: Mapped[int] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        return f"Medicine(id={self.id!r}, title={self.title!r})"
