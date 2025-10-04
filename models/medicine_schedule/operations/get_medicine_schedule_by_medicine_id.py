from sqlalchemy import select

from models.medicine_schedule.medicine_schedule import MedicineSchedule
from services.db.decorators.with_session import with_session


@with_session
def get_medicine_schedule_by_medicine_id(session, medicine_id):
    stmt = select(MedicineSchedule).where(MedicineSchedule.medicine_id.in_([medicine_id]))
    medicine_schedule = session.scalars(stmt).first()
    return medicine_schedule
