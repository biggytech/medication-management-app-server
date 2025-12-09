from flask import Blueprint, request, jsonify

from models.user.operations.create_user import create_user
from models.user.validations import CreateUserValidation
from services.routers.decorators.validate_request import validate_request, BODY

api_sign_up_default = Blueprint('/api/sign-up/default', __name__)


@api_sign_up_default.post('/')
@validate_request(BODY, CreateUserValidation)
def sign_up_default():
    try:
        user_data = request.json

        user_data['is_guest'] = False

        return create_user(**user_data)
    except Exception as e:
        return jsonify({
            'message': '',
            'error': str(e)
        }), 500
