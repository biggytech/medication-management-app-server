from sqlalchemy import select
from sqlalchemy.orm import joinedload

from models.health_tracker.health_tracker import HealthTracker
from services.db.decorators.with_session import with_session


@with_session
def get_health_tracker_by_id(session, health_tracker_id):
    stmt = select(HealthTracker).where(HealthTracker.id.in_([health_tracker_id])).where(
        HealthTracker.deleted_date == None).options(
        joinedload('*'))
    health_tracker = session.scalars(stmt).first()
    return health_tracker
