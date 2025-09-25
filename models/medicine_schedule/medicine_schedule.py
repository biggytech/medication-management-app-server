import datetime
import enum
from dataclasses import dataclass

from sqlalchemy import String, Column, ForeignKey, DateTime, TIMESTAMP, Boolean
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column
from models.base import Base
from sqlalchemy import CheckConstraint
from sqlalchemy.dialects.postgresql import ENUM as pgEnum, JSONB


class MedicineScheduleTypes(str, enum.Enum):
    every_day = "every_day"
    every_other_day = "every_other_day"
    every_x_days = "every_x_days"
    specific_week_days = "specific_week_days"
    only_as_needed = "only_as_needed"

MedicineScheduleTypesType: pgEnum = pgEnum(
    MedicineScheduleTypes,
    name="medicine_schedule_types",
    create_constraint=True,
    metadata=Base.metadata,
    validate_strings=True
)

@dataclass
class MedicineSchedule(Base):
    __tablename__ = "medicine_schedules"
    id: Mapped[int] = mapped_column(primary_key=True)
    medicine_id: Mapped[int] = mapped_column(ForeignKey("medicines.id"))
    type = mapped_column(MedicineScheduleTypesType, nullable=False)
    is_only_as_needed: Mapped[bool] = mapped_column(Boolean())
    every_x_days: Mapped[int] = mapped_column(CheckConstraint("every_x_days >= 0 and every_x_days <= 365")) # 0 for "Only as needed"
    notification_times = mapped_column(JSONB) # 'HH:MM' format, empty for "Only as needed", for "Every Day" its length 1-12, for other options - its length is 1
    user_time_zone: Mapped[str] = mapped_column(String(255)) # needed for notification times handling
    next_dose_date: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)  # manually set date with time set to 0, null for options that do not support manually set date
    dose: Mapped[int] = mapped_column(CheckConstraint("dose >= 1 and dose <= 100"))
    end_date: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    def __repr__(self) -> str:
        return f"Medicine(id={self.id!r}, title={self.title!r})"
