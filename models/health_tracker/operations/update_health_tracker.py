from models.health_tracker.health_tracker import HealthTracker
from models.health_tracker.operations.get_health_tracker_by_id import get_health_tracker_by_id
from models.health_tracker_schedule.health_tracker_schedule import HealthTrackerSchedule
from models.health_tracker_schedule.operations.get_health_tracker_schedule_by_health_tracker_id import \
    get_health_tracker_schedule_by_health_tracker_id
from services.db.decorators.with_session import with_session


@with_session
def update_health_tracker(session, health_tracker, **health_tracker_data):
    # TODO: check existing tracker
    # existing_user = User.query.filter_by(email=user_data['email']).first()
    # if existing_user:
    #     return jsonify({'message': 'User already exists. Please login.'}), 400

    health_tracker_schedule = health_tracker_data.pop('schedule')

    session.query(HealthTracker).filter(HealthTracker.id == health_tracker.id).update(health_tracker_data)

    schedule = get_health_tracker_schedule_by_health_tracker_id(health_tracker.id)
    session.query(HealthTrackerSchedule).filter(HealthTrackerSchedule.id == schedule.id).update(health_tracker_schedule)

    session.commit()

    updated_health_tracker = get_health_tracker_by_id(health_tracker.id)

    return updated_health_tracker
