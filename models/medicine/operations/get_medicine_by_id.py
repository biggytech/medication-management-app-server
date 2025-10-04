from sqlalchemy.orm import joinedload

from models.medicine.medicine import Medicine
from sqlalchemy import select

from services.db.decorators.with_session import with_session

@with_session
def get_medicine_by_id(session, medicine_id):
    stmt = select(Medicine).where(Medicine.id.in_([medicine_id])).options(joinedload('*'))
    medicine = session.scalars(stmt).first()
    return medicine
