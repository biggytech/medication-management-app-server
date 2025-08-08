from flask import Blueprint

from db.utils.with_session import with_session
from services.auth.generate_token import generate_token
from services.models.create_user import create_user
from uuid import uuid4


api_sign_up_anonymous = Blueprint('/api/sign-up/anonymous', __name__)

@api_sign_up_anonymous.post('/')
def sign_up_offline():
    return with_session(__sign_up_offline)

def __sign_up_offline(session):
    uuid = uuid4()

    new_user = create_user(session, full_name="Anonymous User", is_guest=True, uuid=uuid)
    token = generate_token(new_user)

    session.commit()
    session.refresh(new_user)

    return {
        "id": new_user.id,
        "token": token,
        "full_name": new_user.full_name
    }
