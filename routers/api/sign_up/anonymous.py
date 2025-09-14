from flask import Blueprint, request

from db.utils.with_session import with_session
from services.routers.decorators.token_required import token_required
from services.user.create_anonymous_user import create_anonymous_user
from services.user.update_user import update_user

api_sign_up_anonymous = Blueprint('/api/sign-up/anonymous', __name__)

@api_sign_up_anonymous.post('/')
def sign_up_anonymous():
    return create_anonymous_user()

@api_sign_up_anonymous.post('/finish')
@token_required
def sign_up_anonymous_finish(user):
    # TODO: validate user data
    user_data = request.json

    user_data['is_guest'] = False

    return update_user(user, **user_data)

    # return {
    #     "id": 1,
    #     "token": 'aaaa',
    #     "full_name": 'aaaaa444'
    # };
    # return create_anonymous_user()
