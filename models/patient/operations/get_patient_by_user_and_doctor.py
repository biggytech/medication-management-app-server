from sqlalchemy.orm import Session
from typing import Optional
from models.patient.patient import Patient
from services.db.decorators.with_session import with_session


@with_session
def get_patient_by_user_and_doctor(session: Session, user_id: int, doctor_id: int) -> Optional[Patient]:
    """
    Get a patient relationship by user_id and doctor_id.
    Returns the relationship regardless of status (pending, approved, etc.).
    
    Args:
        session: Database session
        user_id: ID of the user (patient)
        doctor_id: ID of the doctor
        
    Returns:
        Patient | None: The patient relationship or None if not found
    """
    patient = session.query(Patient).filter(
        Patient.user_id == user_id,
        Patient.doctor_id == doctor_id
    ).first()
    return patient

