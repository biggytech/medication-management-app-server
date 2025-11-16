from sqlalchemy import select, func, or_
from sqlalchemy.orm import joinedload

from models.doctor.doctor import Doctor
from models.user.user import User
from services.db.decorators.with_session import with_session


@with_session
def get_doctors(session, search=None, page=1, per_page=10):
    """
    Get doctors with optional search and pagination.
    
    Args:
        session: Database session
        search: Optional search query to filter by doctor name, email, specialisation, or place_of_work
        page: Page number (1-indexed)
        per_page: Number of items per page
        
    Returns:
        dict: Dictionary with 'items' (list of doctors) and 'total' (total count)
    """
    # Base query with joined user
    stmt = select(Doctor).options(
        joinedload(Doctor.user)  # Load the related user data
    )
    count_stmt = select(func.count()).select_from(Doctor)
    
    # Apply search filter if provided
    if search:
        # Join User table for search
        search_filter = or_(
            User.full_name.ilike(f'%{search}%'),
            User.email.ilike(f'%{search}%'),
            Doctor.specialisation.ilike(f'%{search}%'),
            Doctor.place_of_work.ilike(f'%{search}%'),
            Doctor.phone.ilike(f'%{search}%')
        )
        stmt = stmt.join(User).where(search_filter)
        count_stmt = count_stmt.join(User, Doctor.user_id == User.id).where(search_filter)
    
    # Get total count
    total = session.scalar(count_stmt)
    
    # Apply pagination
    offset = (page - 1) * per_page
    stmt = stmt.offset(offset).limit(per_page)
    
    # Execute query
    doctors = session.scalars(stmt).all()
    
    return {
        'items': doctors,
        'total': total,
        'page': page,
        'per_page': per_page,
        'pages': (total + per_page - 1) // per_page if total > 0 else 0
    }

