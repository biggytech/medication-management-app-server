from sqlalchemy import select

from models.doctor.doctor import Doctor
from models.user.user import User
from services.db.decorators.with_session import with_session


@with_session
def get_user_by_id(session, user_id):
    stmt = select(User).where(User.id.in_([user_id]))
    user = session.scalars(stmt).first()

    if user:
        # Check if user is a doctor
        doctor_stmt = select(Doctor).where(Doctor.user_id == user_id)
        doctor = session.scalars(doctor_stmt).first()
        is_doctor = doctor is not None

        print('ISSSSSS')
        print(is_doctor)
        user.is_doctor = is_doctor

        # # Convert user to dict and add is_doctor field
        user_dict = {
            'id': user.id,
            'uuid': str(user.uuid),
            'full_name': user.full_name,
            'is_guest': user.is_guest,
            'email': user.email,
            'sex': user.sex,
            'date_of_birth': user.date_of_birth.isoformat() if user.date_of_birth else None,
            'is_doctor': is_doctor
        }
        return user_dict

    return user
