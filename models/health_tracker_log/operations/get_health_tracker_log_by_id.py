from sqlalchemy import select
from sqlalchemy.orm import joinedload

from models.health_tracker_log.health_tracker_log import HealthTrackerLog
from services.db.decorators.with_session import with_session


@with_session
def get_health_tracker_log_by_id(session, health_tracker_log_id):
    stmt = select(HealthTrackerLog).where(HealthTrackerLog.id.in_([health_tracker_log_id])).options(joinedload('*'))
    log = session.scalars(stmt).first()
    return log
