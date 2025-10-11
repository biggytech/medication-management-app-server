from flask import Blueprint, request, jsonify

from models.medication_log.medication_log import MedicationLogTypes
from models.medication_log.operations.create_medication_log import create_medication_log
from models.medication_log.validations import TakeMedicationLogValidation
from services.routers.decorators.token_required import token_required
from services.routers.decorators.validate_request import validate_request, BODY

api_medication_logs = Blueprint('/api/medication-logs', __name__)


@api_medication_logs.post('/<int:medicine_id>/take')
@validate_request(BODY, TakeMedicationLogValidation)
@token_required
def api_medication_logs_take(user, medicine_id):
    # TODO: validate medicine belongs to user
    medication_log_data = request.json
    medication_log_data['medicine_id'] = medicine_id
    medication_log_data['type'] = MedicationLogTypes.taken

    return jsonify(create_medication_log(**medication_log_data))
