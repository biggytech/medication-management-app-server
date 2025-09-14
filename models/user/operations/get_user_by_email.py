from db.utils.with_session import with_session
from models.user.user import User
from sqlalchemy import select

def get_user_by_email(email):
    return with_session(__get_user_by_email, email)

def __get_user_by_email(session, email):
    stmt = select(User).where(User.email.in_([email]))
    user = session.scalars(stmt).first()
    return user
