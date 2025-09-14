from services.auth.generate_token import generate_token
from uuid import uuid4
from models.user.user import User
from werkzeug.security import generate_password_hash

from services.db.decorators.with_session import with_session

@with_session
def create_user(session, **user_data):
    # TODO: check existing user
    # existing_user = User.query.filter_by(email=user_data['email']).first()
    # if existing_user:
    #     return jsonify({'message': 'User already exists. Please login.'}), 400

    uuid = uuid4()

    hashed_password = generate_password_hash(user_data['password'], method="pbkdf2") # "pbkdf2" for MacOS
    user_data['password'] = hashed_password

    new_user = User(
        uuid=uuid,
        **user_data
        # addresses=[Address(email_address="spongebob@sqlalchemy.org")],
    )
    session.add(new_user)

    token = generate_token(new_user)

    session.commit()
    session.refresh(new_user)

    return {
        "id": new_user.id,
        "token": token,
        "full_name": new_user.full_name
    }
