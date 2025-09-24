import datetime
from dataclasses import dataclass
from sqlalchemy import String, Column, ForeignKey, DateTime, TIMESTAMP
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column
from models.base import Base
from sqlalchemy import CheckConstraint

# from models.medicine.medicine import Medicine

@dataclass
class MedicineSetting(Base):
    __tablename__ = "medicine_settings"
    id: Mapped[int] = mapped_column(primary_key=True)
    medicine_id: Mapped[int] = mapped_column(ForeignKey("medicines.id"))
    # medicine: Mapped["Medicine"] = relationship(back_populates="settings")
    dose: Mapped[int] = mapped_column(CheckConstraint("dose >= 1 and dose <= 100"))
    end_date: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    def __repr__(self) -> str:
        return f"Medicine(id={self.id!r}, title={self.title!r})"
