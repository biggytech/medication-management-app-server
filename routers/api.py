from flask import Blueprint

from services.dal.create_user import create_user

api = Blueprint('api', __name__)

@api.post('/sign-up/default')
def sign_up_default():
    return {
        "token": ':TODO'
    }

@api.post('/sign-up/anonymous')
def sign_up_offline():
    create_user(full_name="Anonymous User", is_guest=True)
    return {
        "token": ':TODO',
        "userName": "Anonymous User"
    }

@api.post('/login')
def login():
    return {
        "token": ':TODO',
        "userName": ":TODO"
    }
