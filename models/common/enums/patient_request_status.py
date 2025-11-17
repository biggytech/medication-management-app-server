import enum

from sqlalchemy.dialects.postgresql import ENUM as pgEnum

from models.base import Base


class PatientRequestStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    declined = "declined"


PatientRequestStatusType: pgEnum = pgEnum(
    PatientRequestStatus,
    name="patient_request_status",
    create_constraint=True,
    metadata=Base.metadata,
    validate_strings=True
)

