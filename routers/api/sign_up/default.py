from uuid import uuid4

from flask import Blueprint, request

from db.utils.with_session import with_session
from services.user.create_user import create_user

api_sign_up_default = Blueprint('/api/sign-up/default', __name__)

@api_sign_up_default.post('/')
def sign_up_default():
    user_data = request.json

    user_data['is_guest'] = False

    return with_session(create_user, **user_data)
