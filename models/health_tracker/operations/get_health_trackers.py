from sqlalchemy import select
from sqlalchemy.orm import joinedload

from models.health_tracker.health_tracker import HealthTracker
from services.db.decorators.with_session import with_session


@with_session
def get_health_trackers(session, user_id):
    stmt = (select(HealthTracker).order_by(HealthTracker.id).where(HealthTracker.user_id.in_([user_id]))
            .where(HealthTracker.deleted_date == None)
            .options(joinedload('*')))
    health_trackers = session.scalars(stmt).all()
    return health_trackers
