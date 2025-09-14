from services.auth.get_random_email import get_random_email
from services.auth.get_random_password import get_random_password
from models.user.operations.create_user import create_user

def create_anonymous_user():
    return create_user(
                       full_name="Anonymous User",
                       is_guest=True,
                       password=get_random_password(),
                       email=get_random_email())
