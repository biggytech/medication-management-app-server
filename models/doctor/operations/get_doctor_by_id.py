from sqlalchemy import select
from sqlalchemy.orm import joinedload

from models.doctor.doctor import Doctor
from services.db.decorators.with_session import with_session


@with_session
def get_doctor_by_id(session, doctor_id):
    """
    Get a doctor by their ID.
    
    Args:
        session: Database session
        doctor_id: ID of the doctor to retrieve
        
    Returns:
        Doctor: The doctor object or None if not found
    """
    stmt = select(Doctor).where(Doctor.id == doctor_id).options(
        joinedload('*')  # Load the related user data
    )
    doctor = session.scalars(stmt).first()
    return doctor

