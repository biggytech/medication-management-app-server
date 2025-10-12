import datetime
import enum
from dataclasses import dataclass

from sqlalchemy import ForeignKey, TIMESTAMP, String
from sqlalchemy.dialects.postgresql import ENUM as pgEnum
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from models.base import Base
from models.health_tracker_schedule.health_tracker_schedule import HealthTrackerSchedule


class HealthTrackerTypes(str, enum.Enum):
    blood_pressure = 'blood_pressure'
    heart_rate = 'heart_rate'
    weight = 'weight'
    body_temperature = 'body_temperature'
    menstrual_cycle = 'menstrual_cycle'


HealthTrackerTypesType: pgEnum = pgEnum(
    HealthTrackerTypes,
    name="health_trackers_types",
    create_constraint=True,
    metadata=Base.metadata,
    validate_strings=True
)


@dataclass
class HealthTracker(Base):
    __tablename__ = "health_trackers"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    type: Mapped[str] = mapped_column(HealthTrackerTypesType, nullable=False)
    schedule: Mapped["HealthTrackerSchedule"] = relationship()
    notes: Mapped[str] = mapped_column(String(255), nullable=True)
    deleted_date: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)

    def __repr__(self) -> str:
        return f"HealthTracker(id={self.id!r}, type={self.type!r})"
