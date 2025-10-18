from flask import Blueprint, request, jsonify

from models.user.operations.get_user_by_id import get_user_by_id
from models.user.operations.update_user import update_user
from models.user.validations import UpdateUserValidation
from services.routers.decorators.token_required import token_required
from services.routers.decorators.validate_request import validate_request, BODY

# Create blueprint for user routes
api_users = Blueprint('/api/users', __name__)


@api_users.route('/profile', methods=['GET'])
@token_required
def get_user_profile(user):
    user = get_user_by_id(user.id)
    user_dict = user.as_dict()

    print(user_dict)

    return user_dict


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

        print(user_dict)

        return user_dict


    except Exception as e:
        return jsonify({
            'message': 'Failed to update user profile',
            'error': str(e)
        }), 500
