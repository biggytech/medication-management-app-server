from sqlalchemy.orm import Session, joinedload
from models.patient.patient import Patient
from models.doctor.doctor import Doctor
from services.db.decorators.with_session import with_session


@with_session
def get_patients_by_user_id(session: Session, user_id: int) -> list[Patient]:
    """
    Get all doctors for a specific user (patient).
    
    Args:
        session: Database session
        user_id: ID of the user (patient)
        
    Returns:
        list[Patient]: List of patient relationships for the user
    """
    patients = session.query(Patient).options(
        joinedload(Patient.doctor).joinedload(Doctor.user)
    ).filter(Patient.user_id == user_id).all()
    return patients
