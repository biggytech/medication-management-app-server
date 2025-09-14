from services.auth.generate_token import generate_token
from models.user.user import User
from werkzeug.security import generate_password_hash
from db.utils.with_session import with_session
from services.user.get_user_by_id import get_user_by_id


def update_user(user, **user_data):
    return with_session(__update_user, user, **user_data)

def __update_user(session, user, **user_data):
    # TODO: validate user_data

    # TODO: check existing user
    # existing_user = User.query.filter_by(email=user_data['email']).first()
    # if existing_user:
    #     return jsonify({'message': 'User already exists. Please login.'}), 400

    # uuid = uuid4()

    hashed_password = generate_password_hash(user_data['password'], method="pbkdf2") # "pbkdf2" for MacOS
    user_data['password'] = hashed_password

    session.query(User).filter(User.id == user.id).update(user_data)

    token = generate_token(user)

    session.commit()

    updated_user = get_user_by_id(user.id)

    return {
        "id": updated_user.id,
        "token": token,
        "full_name": updated_user.full_name
    }
