from flask import Blueprint, request, jsonify

from models.health_tracker.operations.create_health_tracker import create_health_tracker
from models.health_tracker.operations.delete_health_tracker_by_id import delete_health_tracker_by_id
from models.health_tracker.operations.get_health_tracker_by_id import get_health_tracker_by_id
from models.health_tracker.operations.get_health_trackers import get_health_trackers
from models.health_tracker.operations.get_health_trackers_by_date import get_health_trackers_by_date
from models.health_tracker.operations.update_health_tracker import update_health_tracker
from models.health_tracker.validations import CreateOrUpdateHealthTrackerValidation
from services.routers.decorators.token_required import token_required
from services.routers.decorators.validate_request import validate_request, BODY

api_health_trackers = Blueprint('/api/health-trackers', __name__)


@api_health_trackers.get('/list')
@token_required
def api_health_trackers_list(user):
    return get_health_trackers(user.id)


@api_health_trackers.get('/list/by-date/<string:utc_date>')
@token_required
def api_health_trackers_list_by_date(user, utc_date):
    # TODO: validate utc_date_time
    timezone = request.args.get('timezone')
    return get_health_trackers_by_date(user.id, utc_date, timezone)


@api_health_trackers.post('/add')
@validate_request(BODY, CreateOrUpdateHealthTrackerValidation)
@token_required
def api_health_trackers_add(user):
    health_tracker_data = request.json
    health_tracker_data['user_id'] = user.id

    return jsonify(create_health_tracker(**health_tracker_data))


@api_health_trackers.get('/<int:health_tracker_id>')
@token_required
def api_health_trackers_get(user, health_tracker_id):
    # TODO: validate medicine belongs to user
    return jsonify(get_health_tracker_by_id(health_tracker_id))


@api_health_trackers.put('/<int:health_tracker_id>')
@validate_request(BODY, CreateOrUpdateHealthTrackerValidation)
@token_required
def api_health_trackers_put(user, health_tracker_id):
    # TODO: validate medicine belongs to user
    health_tracker_data = request.json
    health_tracker = get_health_tracker_by_id(health_tracker_id)

    return jsonify(update_health_tracker(health_tracker=health_tracker, **health_tracker_data))


@api_health_trackers.delete('/<int:health_tracker_id>')
@token_required
def api_health_trackers_delete(user, health_tracker_id):
    # TODO: validate medicine belongs to user
    return jsonify(delete_health_tracker_by_id(health_tracker_id))
