from flask import Blueprint

from services.auth.generate_token import generate_token
from services.models.create_user import create_user

api = Blueprint('api', __name__)

@api.post('/sign-up/default')
def sign_up_default():
    return {
        "token": ':TODO'
    }

@api.post('/sign-up/anonymous')
def sign_up_offline():
    new_user = create_user(full_name="Anonymous User", is_guest=True)
    token = generate_token(new_user)
    return {
        "token": token,
        "userName": new_user.full_name
    }

@api.post('/login')
def login():
    return {
        "token": ':TODO',
        "userName": ":TODO"
    }
