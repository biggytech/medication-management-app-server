from models.user.user import User
from sqlalchemy import select

from services.db.decorators.with_session import with_session
from services.user.get_is_doctor import add_is_doctor_to_user

@with_session
def get_user_by_uuid(session, uuid):
    stmt = select(User).where(User.uuid.in_([uuid]))
    user = session.scalars(stmt).first()
    
    if user:
        # Add is_doctor field to user object
        user = add_is_doctor_to_user(user=user)
    
    return user
