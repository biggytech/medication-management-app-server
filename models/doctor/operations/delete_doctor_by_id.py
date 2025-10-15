from models.doctor.doctor import Doctor
from services.db.decorators.with_session import with_session


@with_session
def delete_doctor_by_id(session, doctor_id):
    """
    Delete a doctor by their ID.
    
    Args:
        session: Database session
        doctor_id: ID of the doctor to delete
        
    Returns:
        dict: Empty dictionary indicating successful deletion
    """
    session.query(Doctor).filter(Doctor.id == doctor_id).delete()
    session.commit()
    
    return {}

