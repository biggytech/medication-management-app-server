from flask import Blueprint

api_login_default = Blueprint('/api/login/default', __name__)

@api_login_default.post('/')
def login():
    return {
        "token": ':TODO',
        "userName": ":TODO"
    }
