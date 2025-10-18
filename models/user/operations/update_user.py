from werkzeug.security import generate_password_hash

from models.user.operations.get_user_by_id import get_user_by_id
from models.user.user import User
from services.db.decorators.with_session import with_session


@with_session
def update_user(session, user, **user_data):
    # TODO: check existing user
    # existing_user = User.query.filter_by(email=user_data['email']).first()
    # if existing_user:
    #     return jsonify({'message': 'User already exists. Please login.'}), 400

    # uuid = uuid4()

    # Only hash password if it's being updated
    if 'password' in user_data and user_data['password']:
        hashed_password = generate_password_hash(user_data['password'], method="pbkdf2")  # "pbkdf2" for MacOS
        user_data['password'] = hashed_password

    # Filter out None values to avoid overwriting with None
    filtered_data = {k: v for k, v in user_data.items() if v is not None}

    session.query(User).filter(User.id == user.id).update(filtered_data)

    session.commit()

    updated_user = get_user_by_id(user.id)

    return updated_user
