from uuid import uuid4

from werkzeug.security import generate_password_hash

from models.user.operations.get_user_by_email import get_user_by_email
from models.user.user import User
from services.auth.generate_token import generate_token
from services.db.decorators.with_session import with_session


@with_session
def create_user(session, **user_data):
    existing_user = get_user_by_email(user_data['email'])
    if existing_user:
        raise ValueError('Пользователь с таким email уже существует!')

    uuid = uuid4()

    hashed_password = generate_password_hash(user_data['password'], method="pbkdf2")  # "pbkdf2" for MacOS
    user_data['password'] = hashed_password

    # Ensure is_guest has a default value if not provided
    if 'is_guest' not in user_data:
        user_data['is_guest'] = False

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
