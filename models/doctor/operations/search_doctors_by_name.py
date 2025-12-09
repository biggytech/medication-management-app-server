from sqlalchemy import select, func
from sqlalchemy.orm import joinedload

from models.doctor.doctor import Doctor
from models.user.user import User
from services.db.decorators.with_session import with_session


@with_session
def search_doctors_by_name(session, name_query, exclude_user_id):
    """
    Search doctors by name using case-insensitive partial matching.
    
    Args:
        session: Database session
        name_query: Search query for doctor's full name
        exclude_user_id
        
    Returns:
        List[Doctor]: List of doctor objects matching the search criteria
    """
    # Create base query with joined user data
    stmt = select(Doctor).options(
        joinedload(Doctor.user)  # Load the related user data
    ).join(User, Doctor.user_id == User.id)

    # Add case-insensitive search filter on user's full_name
    if name_query and name_query.strip():
        search_term = f"%{name_query.strip()}%"
        stmt = stmt.where(
            func.lower(User.full_name).like(func.lower(search_term))
        )

    if exclude_user_id:
        stmt = stmt.where(
            User.id != exclude_user_id
        )

    doctors = session.scalars(stmt).all()
    return doctors
