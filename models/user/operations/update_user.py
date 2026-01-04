from werkzeug.security import generate_password_hash

from models.user.operations.get_user_by_email import get_user_by_email
from models.user.operations.get_user_by_id import get_user_by_id
from models.user.user import User
from services.db.decorators.with_session import with_session


@with_session
def update_user(session, user, **user_data):
    existing_user = get_user_by_email(user_data['email'])
    if existing_user and existing_user.id != user.id:
        raise ValueError('Пользователь с таким email уже существует!')

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
