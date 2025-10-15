from sqlalchemy.orm import Session

from models.patient.patient import Patient
from services.db.decorators.with_session import with_session


@with_session
def get_patient_by_id(session: Session, patient_id: int):
    """
    Get a patient relationship by ID.
    
    Args:
        session: Database session
        patient_id: ID of the patient relationship
        
    Returns:
        Patient | None: The patient relationship or None if not found
    """
    patient = session.query(Patient).filter(Patient.id == patient_id).first()
    return patient
