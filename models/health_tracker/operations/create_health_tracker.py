from models.health_tracker.health_tracker import HealthTracker
from models.health_tracker.operations.get_health_tracker_by_id import get_health_tracker_by_id
from models.health_tracker_schedule.health_tracker_schedule import HealthTrackerSchedule
from services.db.decorators.with_session import with_session


@with_session
def create_health_tracker(session, **health_tracker_data):
    # TODO: check existing tracker
    # existing_user = User.query.filter_by(email=user_data['email']).first()
    # if existing_user:
    #     return jsonify({'message': 'User already exists. Please login.'}), 400

    health_tracker_schedule = health_tracker_data.pop('schedule')

    new_health_tracker = HealthTracker(
        **health_tracker_data,
        schedule=HealthTrackerSchedule(**health_tracker_schedule)
    )
    session.add(new_health_tracker)

    session.commit()
    session.refresh(new_health_tracker)

    return get_health_tracker_by_id(new_health_tracker.id)
