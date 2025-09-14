from models.user.user import User
from db.utils.with_session import with_session
from sqlalchemy import delete

def delete_user(user):
    return with_session(__delete_user, user)

def __delete_user(session, user):
    # TODO: check existing user
    # existing_user = User.query.filter_by(email=user_data['email']).first()
    # if existing_user:
    #     return jsonify({'message': 'User already exists. Please login.'}), 400

    stmt = delete(User).where(User.id.in_([user.id]))
    session.execute(stmt)
    session.commit()

    return {}
