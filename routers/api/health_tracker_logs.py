from flask import Blueprint, request, jsonify

from models.health_tracker_log.operations.create_health_tracker_log import create_health_tracker_log
from models.health_tracker_log.operations.get_health_tracker_logs_by_date import get_health_tracker_logs_by_date
from models.health_tracker_log.validations import AddHealthTrackerLogValidation
from services.routers.decorators.token_required import token_required
from services.routers.decorators.validate_request import validate_request, BODY

api_health_tracker_logs = Blueprint('/api/health-tracker-logs', __name__)


@api_health_tracker_logs.post('/<int:health_tracker_id>/add')
@validate_request(BODY, AddHealthTrackerLogValidation)
@token_required
def api_health_tracker_logs_take(user, health_tracker_id):
    # TODO: validate medicine belongs to user
    health_tracker_log_data = request.json
    health_tracker_log_data['health_tracker_id'] = health_tracker_id

    return jsonify(create_health_tracker_log(**health_tracker_log_data))


@api_health_tracker_logs.get('/list/by-date/<string:utc_date>')
@token_required
def api_health_tracker_logs_list_by_date(user, utc_date):
    # TODO: validate utc_date_time
    timezone = request.args.get('timezone')
    return get_health_tracker_logs_by_date(user.id, utc_date, timezone)
