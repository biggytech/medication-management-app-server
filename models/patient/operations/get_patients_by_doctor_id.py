from sqlalchemy.orm import Session, joinedload

from models.patient.patient import Patient
from services.db.decorators.with_session import with_session


@with_session
def get_patients_by_doctor_id(session: Session, doctor_id: int) -> list[Patient]:
    """
    Get all patients for a specific doctor.
    
    Args:
        session: Database session
        doctor_id: ID of the doctor
        
    Returns:
        list[Patient]: List of patient relationships for the doctor
    """
    patients = session.query(Patient).filter(Patient.doctor_id == doctor_id).options(joinedload('*')).all()
    return patients
