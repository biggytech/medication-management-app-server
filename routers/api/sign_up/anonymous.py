from flask import Blueprint, request

from models.user.validations import CreateUserValidation
from services.routers.decorators.token_required import token_required
from services.routers.decorators.validate_request import validate_request, BODY
from services.user.create_anonymous_user import create_anonymous_user
from services.user.update_user import update_user

api_sign_up_anonymous = Blueprint('/api/sign-up/anonymous', __name__)

@api_sign_up_anonymous.post('/')
def sign_up_anonymous():
    return create_anonymous_user()

@api_sign_up_anonymous.post('/finish')
@validate_request(BODY, CreateUserValidation)
@token_required
def sign_up_anonymous_finish(user):
    user_data = request.json

    user_data['is_guest'] = False

    return update_user(user, **user_data)
