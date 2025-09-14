from models.medicine.medicine import Medicine
from services.auth.generate_token import generate_token
from uuid import uuid4
from models.user.user import User
from werkzeug.security import generate_password_hash
from db.utils.with_session import with_session

def create_medicine(**medicine_data):
    return with_session(__create_medicine, **medicine_data)

def __create_medicine(session, **medicine_data):
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
