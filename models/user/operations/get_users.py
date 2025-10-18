from sqlalchemy import select

from models.user.user import User
from services.db.decorators.with_session import with_session
from services.user.get_is_doctor import add_is_doctor_to_users


@with_session
def get_users(session):
    """
    Get all users.
    
    Args:
        session: Database session
        
    Returns:
        List[User]: List of user objects with is_doctor field added
    """
    stmt = select(User)
    users = session.scalars(stmt).all()
    
    # Add is_doctor field to all users
    users = add_is_doctor_to_users(users=users)
    
    return users
