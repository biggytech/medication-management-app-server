from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash

from services.auth.generate_token import generate_token
from services.user.get_user_by_email import get_user_by_email

api_sign_in_default = Blueprint('/api/sign-in/default', __name__)

@api_sign_in_default.post('/')
def login():
    # TODO: validate user data - fields json/existence only
    user_data = request.json

    user = get_user_by_email(user_data['email'])
    print('user.full_name', user.full_name)

    if not user or not check_password_hash(user.password, user_data['password']):
        # TODO: translate
        return jsonify({'error': 'Invalid email or password'}), 401

    token = generate_token(user)

    return {
        "id": user.id,
        "token": token,
        "full_name": user.full_name
    }
