from models.doctor.doctor import Doctor
from models.doctor.operations.get_doctor_by_id import get_doctor_by_id
from services.db.decorators.with_session import with_session


@with_session
def create_doctor(session, **doctor_data):
    """
    Create a new doctor record.
    
    Args:
        session: Database session
        **doctor_data: Doctor data including user_id, specialisation, place_of_work, photo_url
        
    Returns:
        Doctor: The created doctor object
    """
    # Check if doctor already exists for this user
    existing_doctor = session.query(Doctor).filter(Doctor.user_id == doctor_data['user_id']).first()
    if existing_doctor:
        raise ValueError("Doctor already exists for this user")
    
    new_doctor = Doctor(**doctor_data)
    session.add(new_doctor)
    
    session.commit()
    session.refresh(new_doctor)
    
    return get_doctor_by_id(new_doctor.id)

