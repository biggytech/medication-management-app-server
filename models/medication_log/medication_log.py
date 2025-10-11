import datetime
import enum
from dataclasses import dataclass

from sqlalchemy import ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import ENUM as pgEnum
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from models.base import Base
from models.medicine.medicine import Medicine


class MedicationLogTypes(str, enum.Enum):
    taken = "taken"
    skipped = "skipped"


MedicationLogTypesType: pgEnum = pgEnum(
    MedicationLogTypes,
    name="medication_log_types",
    create_constraint=True,
    metadata=Base.metadata,
    validate_strings=True,
)


class MedicationLogSkipReasons(str, enum.Enum):
    forgot = "forgot"
    ran_out = "ran_out"
    no_need = "no_need"
    side_effects = "side_effects"
    cost_concerns = "cost_concerns"
    not_available = "not_available"
    other = "other"


MedicationLogSkipReasonsType: pgEnum = pgEnum(
    MedicationLogSkipReasons,
    name="medication_log_skip_reasons",
    create_constraint=True,
    metadata=Base.metadata,
    validate_strings=True,
)


@dataclass
class MedicationLog(Base):
    __tablename__ = "medication_logs"
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(MedicationLogTypesType, nullable=False)
    medicine_id: Mapped[int] = mapped_column(ForeignKey("medicines.id"))
    date: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    skip_reason: Mapped[str] = mapped_column(MedicationLogSkipReasonsType, nullable=True)
    medicine: Mapped["Medicine"] = relationship()

    def __repr__(self) -> str:
        return f"Medication Log(id={self.id!r}, type={self.type!r}, date={self.date!r})"
