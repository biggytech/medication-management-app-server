from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash

from models.user.validations import SignInDefaultValidation
from services.auth.generate_token import generate_token
from services.routers.decorators.validate_request import BODY, validate_request
from models.user.operations.get_user_by_email import get_user_by_email

api_sign_in_default = Blueprint('/api/sign-in/default', __name__)

@api_sign_in_default.post('/')
@validate_request(BODY, SignInDefaultValidation)
def login():
    user_data = request.json

    user = get_user_by_email(user_data['email'])

    if not user or not check_password_hash(user.password, user_data['password']):
        # TODO: translate
        return jsonify({'error': 'Invalid email or password'}), 401

    token = generate_token(user)

    return {
        "id": user.id,
        "token": token,
        "full_name": user.full_name
    }
