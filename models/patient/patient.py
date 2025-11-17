from dataclasses import dataclass
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base
from models.user.user import User
from models.doctor.doctor import Doctor
from models.common.enums.patient_request_status import PatientRequestStatus, PatientRequestStatusType


@dataclass
class Patient(Base):
    """
    Patient model to track the relationship between users and doctors.
    This represents a many-to-many relationship where:
    - A doctor can have many patients
    - A patient (user) can have many doctors
    
    Status field tracks the approval state:
    - pending: User has requested to become a patient, waiting for doctor approval
    - approved: Doctor has approved the request, relationship is active
    - declined: Doctor has declined the request (will be removed from DB)
    """
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    doctor_id: Mapped[int] = mapped_column(ForeignKey("doctors.id"))
    status: Mapped[PatientRequestStatus] = mapped_column(
        PatientRequestStatusType,
        nullable=False,
        default=PatientRequestStatus.pending
    )

    # Relationships
    user: Mapped["User"] = relationship("User")
    doctor: Mapped["Doctor"] = relationship("Doctor")

    def __repr__(self) -> str:
        return f"Patient(id={self.id!r}, user_id={self.user_id!r}, doctor_id={self.doctor_id!r}, status={self.status!r})"
