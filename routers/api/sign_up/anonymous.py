from flask import Blueprint, request

from models.user.operations.create_anonymous_user import create_anonymous_user
from models.user.operations.update_user import update_user
from models.user.validations import CreateUserValidation
from services.auth.generate_token import generate_token
from services.routers.decorators.token_required import token_required
from services.routers.decorators.validate_request import validate_request, BODY

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

    updated_user = update_user(user, **user_data)

    token = generate_token(user)

    updated_user.token = token

    return updated_user
