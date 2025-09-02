from flask import Blueprint

from db.utils.with_session import with_session
from services.user.create_anonymous_user import create_anonymous_user

api_sign_up_anonymous = Blueprint('/api/sign-up/anonymous', __name__)

@api_sign_up_anonymous.post('/')
def sign_up_offline():
    return create_anonymous_user()
