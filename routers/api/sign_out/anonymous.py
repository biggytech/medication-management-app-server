from flask import Blueprint

from models.user.operations.delete_user import delete_user
from services.routers.decorators.token_required import token_required

api_sign_out_anonymous = Blueprint('/api/sign-out/anonymous', __name__)

@api_sign_out_anonymous.post('/')
@token_required
def sign_out_anonymous(user):
    return delete_user(user)
