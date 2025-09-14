from db.utils.with_session import with_session
from models.user.user import User
from sqlalchemy import select

def get_user_by_id(id):
    return with_session(__get_user_by_id, id)

def __get_user_by_id(session, id):
    stmt = select(User).where(User.id.in_([id]))
    user = session.scalars(stmt).first()
    return user
