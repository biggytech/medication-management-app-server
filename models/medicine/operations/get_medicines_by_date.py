from sqlalchemy import select, text
from sqlalchemy.orm import joinedload

from models.medicine.medicine import Medicine
from services.db.decorators.with_session import with_session


@with_session
def get_medicines_by_date(session, user_id, utc_date, timezone):
    date_filter = text(
        """
        to_char(next_dose_date at time zone '%s', 'YYYY-MM-DD') <= '%s'
            OR
        (end_date IS NOT NULL AND to_char(end_date at time zone '%s', 'YYYY-MM-DD') = '%s')
        """ % (timezone, utc_date, timezone, utc_date))

    stmt = (select(Medicine)
            .order_by(text('next_dose_date')).where(Medicine.user_id.in_([user_id]))
            .filter(date_filter)
            .options(joinedload('*'))
            )
    medicines = session.scalars(stmt).all()
    return medicines
