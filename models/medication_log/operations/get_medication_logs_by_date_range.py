from sqlalchemy import select, text, and_
from sqlalchemy.orm import joinedload

from models.medication_log.medication_log import MedicationLog
from models.medicine.medicine import Medicine
from services.db.decorators.with_session import with_session


@with_session
def get_medication_logs_by_date_range(session, user_id, start_date, end_date, timezone="UTC"):
    """
    Get medication logs for a user within a date range.
    
    Args:
        session: Database session
        user_id: ID of the user
        start_date: Start date (datetime object)
        end_date: End date (datetime object)
        timezone: Timezone for date filtering (default: UTC)
    
    Returns:
        List of MedicationLog objects with related Medicine data
    """
    # Create filters for user and date range
    user_filter = text("medicines.user_id = :user_id")
    date_filter = text(
        """
        (medication_logs.date at time zone :timezone >= :start_date) AND 
        (medication_logs.date at time zone :timezone <= :end_date)
        """
    )
    
    # Build query with joins to get medicine data
    stmt = (
        select(MedicationLog)
        .join(Medicine, MedicationLog.medicine_id == Medicine.id)
        .filter(user_filter)
        .filter(date_filter)
        .order_by(MedicationLog.date)
        .options(joinedload(MedicationLog.medicine))
    )
    
    # Execute query with parameters
    result = session.execute(stmt, {
        'user_id': user_id,
        'timezone': timezone,
        'start_date': start_date,
        'end_date': end_date
    })
    
    medication_logs = result.scalars().all()
    return medication_logs
