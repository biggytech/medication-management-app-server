from models.user.user import User
from sqlalchemy import delete

from services.db.decorators.with_session import with_session

@with_session
def delete_user(session, user):
    # TODO: check existing user
    # existing_user = User.query.filter_by(email=user_data['email']).first()
    # if existing_user:
    #     return jsonify({'message': 'User already exists. Please login.'}), 400

    stmt = delete(User).where(User.id.in_([user.id]))
    session.execute(stmt)
    session.commit()

    return {}
