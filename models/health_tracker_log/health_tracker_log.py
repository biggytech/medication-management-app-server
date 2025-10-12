import datetime
from dataclasses import dataclass

from sqlalchemy import ForeignKey, TIMESTAMP
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from models.base import Base
from models.health_tracker.health_tracker import HealthTracker


@dataclass
class HealthTrackerLog(Base):
    __tablename__ = "health_tracker_logs"
    id: Mapped[int] = mapped_column(primary_key=True)
    health_tracker_id: Mapped[int] = mapped_column(ForeignKey("health_trackers.id"))
    date: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    value1: Mapped[float] = mapped_column(nullable=False)
    value2: Mapped[float] = mapped_column(nullable=True)
    health_tracker: Mapped["HealthTracker"] = relationship()

    def __repr__(self) -> str:
        return f"HealthTrackerLog(id={self.id!r}, health_tracker_id={self.health_tracker_id!r}, date={self.date!r})"
