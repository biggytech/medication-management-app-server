from flask import Blueprint, request

from models.medicine.operations.create_medicine import create_medicine
from models.medicine.validations import CreateMedicineValidation
from services.routers.decorators.token_required import token_required
from services.routers.decorators.validate_request import validate_request, BODY

api_medicines_add = Blueprint('/api/medicines/add', __name__)

@api_medicines_add.post('/')
@validate_request(BODY, CreateMedicineValidation)
@token_required
def medicines_add(user):
    medicine_data = request.json
    medicine_data.user_id = user.id

    return create_medicine(**medicine_data)
