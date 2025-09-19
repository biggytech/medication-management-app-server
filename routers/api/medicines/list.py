from flask import Blueprint

from models.medicine.operations.get_medicines import get_medicines
from services.routers.decorators.token_required import token_required

api_medicines_list = Blueprint('/api/medicines/list', __name__)

@api_medicines_list.get('/')
@token_required
def medicines_add(user):
    return get_medicines()
