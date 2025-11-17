from sqlalchemy.orm import Session, joinedload

from models.patient.patient import Patient
from models.common.enums.patient_request_status import PatientRequestStatus
from services.db.decorators.with_session import with_session


@with_session
def get_pending_patients_by_doctor_id(session: Session, doctor_id: int) -> list[Patient]:
    """
    Get all pending patient requests for a specific doctor.
    These are requests that are waiting for doctor approval.
    
    Args:
        session: Database session
        doctor_id: ID of the doctor
        
    Returns:
        list[Patient]: List of pending patient relationships for the doctor
    """
    patients = session.query(Patient).filter(
        Patient.doctor_id == doctor_id,
        Patient.status == PatientRequestStatus.pending
    ).options(joinedload('*')).all()
    return patients

