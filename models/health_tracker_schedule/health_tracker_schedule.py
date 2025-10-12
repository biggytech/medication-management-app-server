import datetime
from dataclasses import dataclass

from sqlalchemy import CheckConstraint
from sqlalchemy import String, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from models.base import Base
from models.common.enums.schedule_types import ScheduleTypesType


@dataclass
class HealthTrackerSchedule(Base):
    __tablename__ = "health_tracker_schedules"
    id: Mapped[int] = mapped_column(primary_key=True)
    health_tracker_id: Mapped[int] = mapped_column(ForeignKey("health_trackers.id"))
    type: Mapped[str] = mapped_column(ScheduleTypesType, nullable=False)
    every_x_days: Mapped[int] = mapped_column(
        CheckConstraint("every_x_days >= 0 and every_x_days <= 365"))  # 0 for "Only as needed"
    notification_times: Mapped[list[str]] = mapped_column(
        JSONB)  # 'HH:MM' format, empty for "Only as needed", for "Every Day" its length 1-12, for other options - its length is 1
    user_time_zone: Mapped[str] = mapped_column(String(255))  # needed for notification times handling
    next_take_date: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                              nullable=True)  # null for "Only as needed"
    days_of_week: Mapped[list[int]] = mapped_column(JSONB)
    end_date: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)

    def __repr__(self) -> str:
        return f"HealthTrackerSchedule(id={self.id!r}, type={self.type!r})"
