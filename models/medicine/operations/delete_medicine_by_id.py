import datetime

from models.medicine.medicine import Medicine
from services.db.decorators.with_session import with_session


@with_session
def delete_medicine_by_id(session, medicine_id):
    session.query(Medicine).filter(Medicine.id == medicine_id).update(
        {
            Medicine.deleted_date: datetime.datetime.now()
        }
    )

    session.commit()

    return {}
