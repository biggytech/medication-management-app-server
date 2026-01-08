from flask import Blueprint, request, jsonify

from models.user.operations.get_user_by_email import get_user_by_email
from models.user.operations.get_user_by_id import get_user_by_id
from models.user.operations.update_user import update_user
from models.user.validations import UpdateUserValidation
from services.auth.get_random_password import get_random_password
from services.auth.get_random_verification_code import get_random_verification_code
from services.email.send_password_reset_report import send_password_reset_report
from services.routers.decorators.token_required import token_required
from services.routers.decorators.validate_request import validate_request, BODY

# Create blueprint for user routes
api_users = Blueprint('/api/users', __name__)

users_requested_password_reset = {}


@api_users.route('/profile', methods=['GET'])
@token_required
def get_user_profile(user):
    user = get_user_by_id(user.id)
    user_dict = user.as_dict()

    print(user_dict)

    return user_dict


@api_users.post('/forgot-password')
def forgot_password():
    user_data = request.json

    if not user_data:
        return jsonify({
            'success': False,
            'error': 'Request body is required'
        }), 400

    user = get_user_by_email(user_data['email'])

    if not user:
        return jsonify({'error': 'Неверный email'}), 400

    code = get_random_verification_code()

    users_requested_password_reset[user.email] = code

    send_password_reset_report(email=user.email, code=code)

    return jsonify({'message': 'OK'}), 200


@api_users.post('/confirm-verification-code')
def confirm_verification_code():
    user_data = request.json

    if not user_data:
        return jsonify({
            'success': False,
            'error': 'Request body is required'
        }), 400

    user = get_user_by_email(user_data['email'])

    if not user:
        return jsonify({'error': 'Неверный email'}), 400

    expected_code = users_requested_password_reset[user.email]

    if not expected_code:
        return jsonify({'error': 'Неверный email'}), 400

    if expected_code != user_data['code']:
        return jsonify({'error': 'Неверный код'}), 400

    return jsonify({'message': 'OK'}), 200


@api_users.post('/update-forgotten-password')
def update_forgotten_password():
    user_data = request.json

    if not user_data:
        return jsonify({
            'success': False,
            'error': 'Request body is required'
        }), 400

    user = get_user_by_email(user_data['email'])

    if not user:
        return jsonify({'error': 'Неверный email'}), 400

    expected_code = users_requested_password_reset[user.email]

    if not expected_code:
        return jsonify({'error': 'Неверный email'}), 400

    if expected_code != user_data['code']:
        return jsonify({'error': 'Неверный код'}), 400

    update_user(user=user, password=user_data['password'], email=user.email)

    del users_requested_password_reset[user.email]

    return jsonify({'message': 'OK'}), 200


@api_users.route('/profile', methods=['PUT'])
@validate_request(BODY, UpdateUserValidation)
@token_required
def update_user_profile(user):
    """
    Update user profile information
    Allows users to update their name, email, password, sex, and date of birth
    """
    try:
        # Get the request data
        user_data = request.get_json()

        # Update the user
        result = update_user(user, **user_data)

        user = get_user_by_id(user.id)
        user_dict = user.as_dict()

        return user_dict


    except Exception as e:
        return jsonify({
            'message': 'Failed to update user profile',
            'error': str(e)
        }), 500
