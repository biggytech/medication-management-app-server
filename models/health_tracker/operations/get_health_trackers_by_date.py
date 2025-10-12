from sqlalchemy import select, text
from sqlalchemy.orm import joinedload

from models.health_tracker.health_tracker import HealthTracker
from services.db.decorators.with_session import with_session


@with_session
def get_health_trackers_by_date(session, user_id, utc_date, timezone):
    date_filter = text(
        """
        (
            (
                to_char(next_take_date at time zone '%s', 'YYYY-MM-DD') <= '%s'
                AND (
                    end_date IS NULL OR to_char(end_date at time zone '%s', 'YYYY-MM-DD') >= '%s'
                )
            )
            OR
            (end_date IS NOT NULL AND to_char(end_date at time zone '%s', 'YYYY-MM-DD') = '%s')
        )
        """ % (timezone, utc_date, timezone, utc_date, timezone, utc_date))

    stmt = (select(HealthTracker)
            .order_by(text('next_take_date')).where(HealthTracker.user_id.in_([user_id]))
            .where(HealthTracker.deleted_date == None)
            .filter(date_filter)
            .options(joinedload('*'))
            )
    health_trackers = session.scalars(stmt).all()
    return health_trackers
