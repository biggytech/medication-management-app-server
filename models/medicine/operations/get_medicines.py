from sqlalchemy import select
from sqlalchemy.orm import joinedload

from models.medicine.medicine import Medicine
from services.db.decorators.with_session import with_session


@with_session
def get_medicines(session, user_id):
    stmt = (select(Medicine).order_by(Medicine.id).where(Medicine.user_id.in_([user_id]))
            .where(Medicine.deleted_date == None)
            .options(joinedload('*')))
    medicines = session.scalars(stmt).all()
    return medicines
