from sqlalchemy import select

from models.medication_log.medication_log import MedicationLog
from services.db.decorators.with_session import with_session


@with_session
def get_medication_log_by_id(session, medication_log_id):
    stmt = select(MedicationLog).where(MedicationLog.id.in_([medication_log_id]))
    medication_log = session.scalars(stmt).first()
    return medication_log
