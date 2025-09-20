from dataclasses import dataclass
from sqlalchemy import String, Column
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from models.base import Base
import enum
from sqlalchemy.dialects.postgresql import ENUM as pgEnum

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
    __tablename__ = "medicine"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    form = mapped_column(MedicineFormsType, nullable=False)
    def __repr__(self) -> str:
        return f"Medicine(id={self.id!r}, title={self.title!r})"
