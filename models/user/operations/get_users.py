from sqlalchemy import select, func, or_

from models.user.user import User
from services.db.decorators.with_session import with_session
from services.user.get_is_doctor import add_is_doctor_to_users


@with_session
def get_users(session, search=None, page=1, per_page=10):
    """
    Get users with optional search and pagination.
    
    Args:
        session: Database session
        search: Optional search query to filter by full_name or email
        page: Page number (1-indexed)
        per_page: Number of items per page
        
    Returns:
        dict: Dictionary with 'items' (list of users) and 'total' (total count)
    """
    # Base query
    stmt = select(User)
    count_stmt = select(func.count()).select_from(User)
    
    # Apply search filter if provided
    if search:
        search_filter = or_(
            User.full_name.ilike(f'%{search}%'),
            User.email.ilike(f'%{search}%')
        )
        stmt = stmt.where(search_filter)
        count_stmt = count_stmt.where(search_filter)
    
    # Get total count
    total = session.scalar(count_stmt)
    
    # Apply pagination
    offset = (page - 1) * per_page
    stmt = stmt.offset(offset).limit(per_page)
    
    # Execute query
    users = session.scalars(stmt).all()
    
    # Add is_doctor field to all users
    users = add_is_doctor_to_users(users=users)
    
    return {
        'items': users,
        'total': total,
        'page': page,
        'per_page': per_page,
        'pages': (total + per_page - 1) // per_page if total > 0 else 0
    }
