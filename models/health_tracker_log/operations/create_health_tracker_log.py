from models.health_tracker_log.health_tracker_log import HealthTrackerLog
from models.health_tracker_log.operations.get_health_tracker_log_by_id import get_health_tracker_log_by_id
from services.db.decorators.with_session import with_session


@with_session
def create_health_tracker_log(session, **health_tracker_log_data):
    new_health_tracker_log = HealthTrackerLog(
        **health_tracker_log_data,
    )
    session.add(new_health_tracker_log)

    session.commit()
    session.refresh(new_health_tracker_log)

    return get_health_tracker_log_by_id(new_health_tracker_log.id)
