from sqlalchemy import select

from models.health_tracker_schedule.health_tracker_schedule import HealthTrackerSchedule
from services.db.decorators.with_session import with_session


@with_session
def get_health_tracker_schedule_by_health_tracker_id(session, health_tracker_id):
    stmt = select(HealthTrackerSchedule).where(HealthTrackerSchedule.health_tracker_id.in_([health_tracker_id]))
    schedule = session.scalars(stmt).first()
    return schedule
