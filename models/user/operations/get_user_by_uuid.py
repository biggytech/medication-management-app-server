from db.utils.with_session import with_session
from models.user.user import User
from sqlalchemy import select

def get_user_by_uuid(uuid):
    return with_session(__get_user_by_uuid, uuid)

def __get_user_by_uuid(session, uuid):
    stmt = select(User).where(User.uuid.in_([uuid]))
    user = session.scalars(stmt).first()
    return user
