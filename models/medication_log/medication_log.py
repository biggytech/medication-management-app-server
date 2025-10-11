import datetime
from dataclasses import dataclass

from sqlalchemy import ForeignKey, TIMESTAMP
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from models.base import Base


@dataclass
class MedicationLog(Base):
    __tablename__ = "medication_logs"
    id: Mapped[int] = mapped_column(primary_key=True)
    medicine_id: Mapped[int] = mapped_column(ForeignKey("medicines.id"))
    date: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)

    def __repr__(self) -> str:
        return f"Medication Log(id={self.id!r}, date={self.date!r})"
