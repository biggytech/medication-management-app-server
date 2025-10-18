from sqlalchemy import select

from models.user.user import User
from services.db.decorators.with_session import with_session


@with_session
def get_user_by_id(session, user_id):
    stmt = select(User).where(User.id.in_([user_id]))
    user = session.scalars(stmt).first()

    # if user:
    # Add is_doctor field to user object
    # user = add_is_doctor_to_user(user=user)

    return user
