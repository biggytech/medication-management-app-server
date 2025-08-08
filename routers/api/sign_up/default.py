from uuid import uuid4

from flask import Blueprint, request

from db.utils.with_session import with_session
from services.auth.generate_token import generate_token
from services.models.create_user import create_user

api_sign_up_default = Blueprint('/api/sign-up/default', __name__)

@api_sign_up_default.post('/')
def sign_up_default():
    user_data = request.json
    return with_session(__sign_up_default, user_data)

def __sign_up_default(session, user_data):
    uuid = uuid4()

    new_user = create_user(session, uuid=uuid, **user_data)
    token = generate_token(new_user)

    session.commit()
    session.refresh(new_user)

    return {
        "id": new_user.id,
        "token": token,
        "full_name": new_user.full_name
    }
