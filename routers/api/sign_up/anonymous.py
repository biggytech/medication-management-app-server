from flask import Blueprint

from services.auth.generate_token import generate_token
from services.models.create_user import create_user

api_sign_up_anonymous = Blueprint('/api/sign-up/anonymous', __name__)

@api_sign_up_anonymous.post('/')
def sign_up_offline():
    new_user = create_user(full_name="Anonymous User", is_guest=True)
    token = generate_token(new_user)
    return {
        "token": token,
        "userName": new_user.full_name
    }
