from sqlalchemy.orm import Session
from models.patient.patient import Patient
from models.common.enums.patient_request_status import PatientRequestStatus
from services.db.decorators.with_session import with_session


@with_session
def decline_patient(session: Session, patient_id: int, doctor_id: int) -> bool:
    """
    Decline a pending patient request.
    Removes the patient relationship from the database.
    
    Args:
        session: Database session
        patient_id: ID of the patient relationship
        doctor_id: ID of the doctor (for validation)
        
    Returns:
        bool: True if successfully declined and deleted
        
    Raises:
        ValueError: If patient doesn't exist, doesn't belong to doctor, or is not pending
    """
    # Get the patient relationship
    patient = session.query(Patient).filter(Patient.id == patient_id).first()
    
    if not patient:
        raise ValueError(f"Patient relationship with id {patient_id} not found")
    
    # Verify it belongs to the doctor
    if patient.doctor_id != doctor_id:
        raise ValueError(f"Patient relationship does not belong to doctor {doctor_id}")
    
    # Verify it's pending
    if patient.status != PatientRequestStatus.pending:
        raise ValueError(f"Patient relationship is not pending (current status: {patient.status})")
    
    # Delete the patient relationship
    session.delete(patient)
    session.commit()
    
    return True

