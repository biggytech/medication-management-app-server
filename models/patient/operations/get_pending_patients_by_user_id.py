from sqlalchemy.orm import Session, joinedload
from models.patient.patient import Patient
from models.doctor.doctor import Doctor
from models.common.enums.patient_request_status import PatientRequestStatus
from services.db.decorators.with_session import with_session


@with_session
def get_pending_patients_by_user_id(session: Session, user_id: int) -> list[Patient]:
    """
    Get all pending patient requests for a specific user (patient).
    These are requests that the user has sent and are waiting for doctor approval.
    
    Args:
        session: Database session
        user_id: ID of the user (patient)
        
    Returns:
        list[Patient]: List of pending patient relationships for the user
    """
    patients = session.query(Patient).options(
        joinedload(Patient.doctor).joinedload(Doctor.user)
    ).filter(
        Patient.user_id == user_id,
        Patient.status == PatientRequestStatus.pending
    ).all()
    return patients

