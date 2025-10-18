"""
Utility function to check if a user is a doctor and add is_doctor field to user objects.
"""

from sqlalchemy import select
from models.doctor.doctor import Doctor
from services.db.decorators.with_session import with_session


@with_session
def get_is_doctor(session, user_id):
    """
    Check if a user is a doctor by their user ID.
    
    Args:
        session: Database session
        user_id: ID of the user to check
        
    Returns:
        bool: True if user is a doctor, False otherwise
    """
    doctor_stmt = select(Doctor).where(Doctor.user_id == user_id)
    doctor = session.scalars(doctor_stmt).first()
    return doctor is not None


@with_session
def add_is_doctor_to_user(session, user):
    """
    Add is_doctor field to a user object.
    
    Args:
        session: Database session
        user: User object to add is_doctor field to
        
    Returns:
        User: User object with is_doctor field added
    """
    if user:
        is_doctor = get_is_doctor(user_id=user.id)
        user.is_doctor = is_doctor
    return user


@with_session
def add_is_doctor_to_users(session, users):
    """
    Add is_doctor field to a list of user objects.
    
    Args:
        session: Database session
        users: List of User objects to add is_doctor field to
        
    Returns:
        list: List of User objects with is_doctor field added
    """
    if users:
        for user in users:
            is_doctor = get_is_doctor(user_id=user.id)
            user.is_doctor = is_doctor
    return users
