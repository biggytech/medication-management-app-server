from models.doctor.doctor import Doctor
from models.doctor.operations.get_doctor_by_id import get_doctor_by_id
from services.db.decorators.with_session import with_session


@with_session
def update_doctor(session, doctor, **doctor_data):
    """
    Update an existing doctor record.
    
    Args:
        session: Database session
        doctor: The doctor object to update
        **doctor_data: Updated doctor data (specialisation, place_of_work, photo_url)
        
    Returns:
        Doctor: The updated doctor object
    """
    # Update only the provided fields
    session.query(Doctor).filter(Doctor.id == doctor.id).update(doctor_data)
    session.commit()

    # Return the updated doctor
    updated_doctor = get_doctor_by_id(doctor.id)
    return updated_doctor

