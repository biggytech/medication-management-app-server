from sqlalchemy.orm import Session
from models.patient.patient import Patient
from models.common.enums.patient_request_status import PatientRequestStatus
from services.db.decorators.with_session import with_session


@with_session
def cancel_pending_request(session: Session, user_id: int, doctor_id: int) -> bool:
    """
    Cancel a pending patient request.
    Removes the pending patient relationship from the database.
    Only works for pending requests - approved relationships cannot be canceled this way.
    
    Args:
        session: Database session
        user_id: ID of the user (patient) who sent the request
        doctor_id: ID of the doctor
        
    Returns:
        bool: True if successfully canceled and deleted
        
    Raises:
        ValueError: If patient doesn't exist, doesn't belong to user, or is not pending
    """
    # Get the patient relationship
    patient = session.query(Patient).filter(
        Patient.user_id == user_id,
        Patient.doctor_id == doctor_id
    ).first()
    
    if not patient:
        raise ValueError(f"Patient relationship not found between user {user_id} and doctor {doctor_id}")
    
    # Verify it's pending
    if patient.status != PatientRequestStatus.pending:
        raise ValueError(f"Patient relationship is not pending (current status: {patient.status})")
    
    # Delete the patient relationship
    session.delete(patient)
    session.commit()
    
    return True

