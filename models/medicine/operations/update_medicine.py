from models.medicine.medicine import Medicine
from models.medicine.operations.get_medicine_by_id import get_medicine_by_id
from models.medicine_schedule.medicine_schedule import MedicineSchedule
from models.medicine_schedule.operations.get_medicine_schedule_by_medicine_id import \
    get_medicine_schedule_by_medicine_id
from services.db.decorators.with_session import with_session


@with_session
def update_medicine(session, medicine, **medicine_data):
    # TODO: check existing medicine
    # existing_user = User.query.filter_by(email=user_data['email']).first()
    # if existing_user:
    #     return jsonify({'message': 'User already exists. Please login.'}), 400

    medicine_schedule = medicine_data.pop('schedule')

    session.query(Medicine).filter(Medicine.id == medicine.id).update(medicine_data)

    schedule = get_medicine_schedule_by_medicine_id(medicine.id)
    session.query(MedicineSchedule).filter(MedicineSchedule.id == schedule.id).update(medicine_schedule)

    session.commit()

    updated_medicine = get_medicine_by_id(medicine.id)

    return updated_medicine
