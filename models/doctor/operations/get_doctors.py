from sqlalchemy import select
from sqlalchemy.orm import joinedload

from models.doctor.doctor import Doctor
from services.db.decorators.with_session import with_session


@with_session
def get_doctors(session):
    """
    Get all doctors with optional pagination.
    
    Args:
        session: Database session
        limit: Maximum number of doctors to return (optional)
        offset: Number of doctors to skip (default: 0)
        
    Returns:
        List[Doctor]: List of doctor objects
    """
    stmt = select(Doctor).options(
        joinedload(Doctor.user)  # Load the related user data
    )

    doctors = session.scalars(stmt).all()
    return doctors

