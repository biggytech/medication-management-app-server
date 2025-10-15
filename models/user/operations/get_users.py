from sqlalchemy import select

from models.user.user import User
from services.db.decorators.with_session import with_session


@with_session
def get_users(session):
    """
    Get all users.
    
    Args:
        session: Database session
        
    Returns:
        List[User]: List of user objects
    """
    stmt = select(User)
    users = session.scalars(stmt).all()
    return users
