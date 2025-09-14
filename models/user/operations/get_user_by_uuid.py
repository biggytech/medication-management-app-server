from models.user.user import User
from sqlalchemy import select

from services.db.decorators.with_session import with_session

@with_session
def get_user_by_uuid(session, uuid):
    stmt = select(User).where(User.uuid.in_([uuid]))
    user = session.scalars(stmt).first()
    return user
