import datetime

from models.health_tracker.health_tracker import HealthTracker
from services.db.decorators.with_session import with_session


@with_session
def delete_health_tracker_by_id(session, health_tracker_id):
    session.query(HealthTracker).filter(HealthTracker.id == health_tracker_id).update(
        {
            HealthTracker.deleted_date: datetime.datetime.now()
        }
    )

    session.commit()

    return {}
