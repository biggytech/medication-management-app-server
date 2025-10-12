from sqlalchemy import select
from sqlalchemy.orm import joinedload

from models.doctor.doctor import Doctor
from services.db.decorators.with_session import with_session


@with_session
def get_doctor_by_user_id(session, user_id):
    """
    Get a doctor by their user ID.
    
    Args:
        session: Database session
        user_id: ID of the user linked to the doctor
        
    Returns:
        Doctor: The doctor object or None if not found
    """
    stmt = select(Doctor).where(Doctor.user_id == user_id).options(
        joinedload('*')  # Load the related user data
    )
    doctor = session.scalars(stmt).first()
    return doctor
