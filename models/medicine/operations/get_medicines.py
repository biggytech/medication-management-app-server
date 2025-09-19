from models.medicine.medicine import Medicine
from services.db.decorators.with_session import with_session
from sqlalchemy import select

@with_session
def get_medicines(session):
    stmt = select(Medicine).order_by(Medicine.id)
    medicines = session.scalars(stmt).all()
    return medicines
