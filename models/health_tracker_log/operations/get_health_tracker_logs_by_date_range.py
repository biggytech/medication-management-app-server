from sqlalchemy import select, text
from sqlalchemy.orm import joinedload

from models.health_tracker_log.health_tracker_log import HealthTrackerLog
from models.health_tracker.health_tracker import HealthTracker
from services.db.decorators.with_session import with_session


@with_session
def get_health_tracker_logs_by_date_range(session, user_id, start_date, end_date, timezone="UTC"):
    """
    Get health tracker logs for a user within a date range.
    
    Args:
        session: Database session
        user_id: ID of the user
        start_date: Start date (datetime object)
        end_date: End date (datetime object)
        timezone: Timezone for date filtering (default: UTC)
    
    Returns:
        List of HealthTrackerLog objects with related HealthTracker data
    """
    # Create filters for user and date range
    user_filter = text("health_trackers.user_id = :user_id")
    date_filter = text(
        """
        (health_tracker_logs.date at time zone :timezone >= :start_date) AND 
        (health_tracker_logs.date at time zone :timezone <= :end_date)
        """
    )
    
    # Build query with joins to get health tracker data
    stmt = (
        select(HealthTrackerLog)
        .join(HealthTracker, HealthTrackerLog.health_tracker_id == HealthTracker.id)
        .filter(user_filter)
        .filter(date_filter)
        .order_by(HealthTrackerLog.date)
        .options(joinedload(HealthTrackerLog.health_tracker))
    )
    
    # Execute query with parameters
    result = session.execute(stmt, {
        'user_id': user_id,
        'timezone': timezone,
        'start_date': start_date,
        'end_date': end_date
    })
    
    health_tracker_logs = result.scalars().all()
    return health_tracker_logs
