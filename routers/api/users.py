from flask import Blueprint, request, jsonify

from models.user.operations.update_user import update_user
from models.user.validations import UpdateUserValidation
from services.routers.decorators.token_required import token_required
from services.routers.decorators.validate_request import validate_request, BODY

# Create blueprint for user routes
api_users = Blueprint('/api/users', __name__)


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

        return jsonify({
            'message': 'User profile updated successfully',
            'user': result
        }), 200

    except Exception as e:
        return jsonify({
            'message': 'Failed to update user profile',
            'error': str(e)
        }), 500
