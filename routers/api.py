from flask import Blueprint

api = Blueprint('api', __name__)

@api.post('/sign-up/default')
def sign_up_default():
    return {
        "token": ':TODO'
    }

@api.post('/sign-up/offline')
def sign_up_offline():
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
