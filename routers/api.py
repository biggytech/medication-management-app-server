from flask import Blueprint

api = Blueprint('api', __name__)

@api.route('/login')
def login():
    return "API - Login"
