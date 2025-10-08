from models.medicine.medicine import Medicine
from models.medicine.operations.get_medicine_by_id import get_medicine_by_id
from models.medicine_schedule.medicine_schedule import MedicineSchedule
from services.db.decorators.with_session import with_session


@with_session
def create_medicine(session, **medicine_data):
    # TODO: check existing medicine
    # existing_user = User.query.filter_by(email=user_data['email']).first()
    # if existing_user:
    #     return jsonify({'message': 'User already exists. Please login.'}), 400

    medicine_schedule = medicine_data.pop('schedule')

    new_medicine = Medicine(
        **medicine_data,
        schedule=MedicineSchedule(**medicine_schedule)
    )
    session.add(new_medicine)

    session.commit()
    session.refresh(new_medicine)

    return get_medicine_by_id(new_medicine.id)
