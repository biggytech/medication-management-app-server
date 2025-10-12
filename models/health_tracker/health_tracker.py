import enum
from dataclasses import dataclass

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import ENUM as pgEnum
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from models.base import Base


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

    # every_x_days: Mapped[int] = mapped_column(
    #     CheckConstraint("every_x_days >= 0 and every_x_days <= 365"))  # 0 for "Only as needed"
    # notification_times: Mapped[list[str]] = mapped_column(
    #     JSONB)  # 'HH:MM' format, empty for "Only as needed", for "Every Day" its length 1-12, for other options - its length is 1
    # user_time_zone: Mapped[str] = mapped_column(String(255))  # needed for notification times handling
    # next_take_date: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),
    #                                                           nullable=True)  # null for "Only as needed"
    # days_of_week: Mapped[list[int]] = mapped_column(JSONB)
    # dose: Mapped[int] = mapped_column(CheckConstraint("dose >= 1 and dose <= 100"))
    # end_date: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)

    def __repr__(self) -> str:
        return f"Medicine(id={self.id!r}, type={self.type!r})"
