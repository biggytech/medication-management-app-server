from sqlalchemy import delete

from models.user.user import User
from services.db.decorators.with_session import with_session


@with_session
def delete_user(session, user):
    # TODO: cascade delete?
    stmt = delete(User).where(User.id.in_([user.id]))
    session.execute(stmt)
    session.commit()

    return {}
