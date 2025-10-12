from sqlalchemy import select, text
from sqlalchemy.orm import joinedload

from models.health_tracker_log.health_tracker_log import HealthTrackerLog
from services.db.decorators.with_session import with_session


@with_session
def get_health_tracker_logs_by_date(session, user_id, utc_date, timezone):
    user_filter = text(
        """
        (user_id = %s)
        """ % (user_id)
    )

    date_filter = text(
        """
        (to_char(date at time zone '%s', 'YYYY-MM-DD') = '%s')
        """ % (timezone, utc_date))

    stmt = (select(HealthTrackerLog)
            .order_by(text('date'))
            .filter(user_filter)
            .filter(date_filter)
            .options(joinedload('*'))
            )
    logs = session.scalars(stmt).all()
    return logs
