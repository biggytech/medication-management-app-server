from models.user.user import User
from sqlalchemy import select

from services.db.decorators.with_session import with_session

@with_session
def get_user_by_id(session, id):
    stmt = select(User).where(User.id.in_([id]))
    user = session.scalars(stmt).first()
    return user
