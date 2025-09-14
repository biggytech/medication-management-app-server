from models.medicine.medicine import Medicine
from services.db.decorators.with_session import with_session

@with_session
def create_medicine(session, **medicine_data):
    # TODO: check existing medicine
    # existing_user = User.query.filter_by(email=user_data['email']).first()
    # if existing_user:
    #     return jsonify({'message': 'User already exists. Please login.'}), 400

    new_medicine = Medicine(
        **medicine_data
    )
    session.add(new_medicine)

    session.commit()
    # session.refresh(new_user)

    return {

    }
