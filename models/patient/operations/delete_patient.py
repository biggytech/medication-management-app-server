from sqlalchemy.orm import Session
from models.patient.patient import Patient
from services.db.decorators.with_session import with_session


@with_session
def delete_patient(session: Session, user_id: int, doctor_id: int) -> bool:
    """
    Delete a patient-doctor relationship.
    
    Args:
        session: Database session
        user_id: ID of the user (patient)
        doctor_id: ID of the doctor
        
    Returns:
        bool: True if relationship was deleted, False if not found
    """
    patient = session.query(Patient).filter(
        Patient.user_id == user_id,
        Patient.doctor_id == doctor_id
    ).first()
    
    if not patient:
        return False
    
    session.delete(patient)
    session.commit()
    return True
