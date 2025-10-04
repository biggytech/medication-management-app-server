from flask import Blueprint, request, jsonify

from models.medicine.operations.create_medicine import create_medicine
from models.medicine.operations.get_medicine_by_id import get_medicine_by_id
from models.medicine.operations.get_medicines import get_medicines
from models.medicine.operations.update_medicine import update_medicine
from models.medicine.validations import CreateOrUpdateMedicineValidation
from services.routers.decorators.token_required import token_required
from services.routers.decorators.validate_request import validate_request, BODY

api_medicines = Blueprint('/api/medicines', __name__)


@api_medicines.get('/list')
@token_required
def api_medicines_list(user):
    return get_medicines(user.id)


@api_medicines.post('/add')
@validate_request(BODY, CreateOrUpdateMedicineValidation)
@token_required
def api_medicines_add(user):
    medicine_data = request.json
    medicine_data['user_id'] = user.id

    return create_medicine(**medicine_data)


@api_medicines.get('/<int:medicine_id>')
@token_required
def api_medicines_get(user, medicine_id):
    # TODO: validate medicine belongs to user
    return jsonify(get_medicine_by_id(medicine_id))


@api_medicines.put('/<int:medicine_id>')
@validate_request(BODY, CreateOrUpdateMedicineValidation)
@token_required
def api_medicines_put(user, medicine_id):
    # TODO: validate medicine belongs to user
    medicine_data = request.json
    medicine = get_medicine_by_id(medicine_id)

    return jsonify(update_medicine(medicine=medicine, **medicine_data))
