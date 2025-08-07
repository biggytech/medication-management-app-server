from flask import Blueprint

api_sign_up_default = Blueprint('/api/sign-up/default', __name__)

@api_sign_up_default.post('/')
def sign_up_default():
    return {
        "token": ':TODO'
    }
