from models.medication_log.medication_log import MedicationLog
from models.medication_log.operations.get_medication_log_by_id import get_medication_log_by_id
from services.db.decorators.with_session import with_session


@with_session
def create_medication_log(session, **medication_log_data):
    # TODO: check existing medicine
    # existing_user = User.query.filter_by(email=user_data['email']).first()
    # if existing_user:
    #     return jsonify({'message': 'User already exists. Please login.'}), 400

    new_medication_log = MedicationLog(
        **medication_log_data,
    )
    session.add(new_medication_log)

    session.commit()
    session.refresh(new_medication_log)

    return get_medication_log_by_id(new_medication_log.id)
