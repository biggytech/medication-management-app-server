from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc
from models.chat_message.chat_message import ChatMessage
from models.user.user import User
from models.doctor.doctor import Doctor
from models.patient.patient import Patient
from models.common.enums.patient_request_status import PatientRequestStatus
from typing import List, Dict
from services.db.decorators.with_session import with_session


@with_session
def get_user_conversations(session: Session, user_id: int) -> List[Dict]:
    """
    Get all conversations for a user with the last message and unread count.
    
    Args:
        session: Database session
        user_id: ID of the user
        
    Returns:
        List of conversation dictionaries with other user info and last message
    """
    # Get all messages involving this user
    all_messages = session.query(ChatMessage).filter(
        or_(
            ChatMessage.sender_id == user_id,
            ChatMessage.receiver_id == user_id
        )
    ).order_by(desc(ChatMessage.created_at)).all()
    
    # Group messages by conversation (other user)
    conversations_dict = {}
    
    for message in all_messages:
        # Determine the other user in this conversation
        other_user_id = message.sender_id if message.sender_id != user_id else message.receiver_id
        
        # If we haven't seen this conversation yet, or this message is newer
        if other_user_id not in conversations_dict:
            conversations_dict[other_user_id] = {
                'last_message': message,
                'unread_count': 0
            }
    
    # Get user details for all other users
    other_user_ids = list(conversations_dict.keys())
    if not other_user_ids:
        return []
    
    users = session.query(User).filter(User.id.in_(other_user_ids)).all()
    user_dict = {user.id: user for user in users}
    
    # Get doctor information for users who are doctors
    doctors = session.query(Doctor).filter(Doctor.user_id.in_(other_user_ids + [user_id])).all()
    doctor_dict = {doctor.user_id: doctor for doctor in doctors}
    
    # Get all approved patient relationships involving the current user
    # Only show conversations between users who have an approved patient-doctor relationship
    approved_patients = session.query(Patient).filter(
        Patient.status == PatientRequestStatus.approved
    ).all()
    
    # Create a set of valid conversation user pairs
    valid_conversations = set()
    current_user_doctor = next((d for d in doctors if d.user_id == user_id), None)
    
    for patient in approved_patients:
        patient_doctor = next((d for d in doctors if d.id == patient.doctor_id), None)
        if not patient_doctor:
            continue
            
        # If current user is the doctor and other user is the patient
        if current_user_doctor and patient.doctor_id == current_user_doctor.id:
            valid_conversations.add(patient.user_id)
        # If current user is the patient and other user is their doctor
        elif patient.user_id == user_id:
            valid_conversations.add(patient_doctor.user_id)
    
    # Calculate unread counts and format results
    result = []
    for other_user_id, conv_data in conversations_dict.items():
        other_user = user_dict.get(other_user_id)
        if not other_user:
            continue
        
        # Filter: only include conversations with approved patient-doctor relationships
        if other_user_id not in valid_conversations:
            continue
            
        # Count unread messages for this conversation
        unread_count = session.query(ChatMessage).filter(
            and_(
                or_(
                    and_(ChatMessage.sender_id == user_id, ChatMessage.receiver_id == other_user_id),
                    and_(ChatMessage.sender_id == other_user_id, ChatMessage.receiver_id == user_id)
                ),
                ChatMessage.receiver_id == user_id,
                ChatMessage.is_read == False
            )
        ).count()
        
        # Check if this user is a doctor and has a photo
        doctor = doctor_dict.get(other_user_id)
        photo_url = doctor.photo_url if doctor and doctor.photo_url else None
        
        result.append({
            'other_user_id': other_user_id,
            'other_user_name': other_user.full_name,
            'last_message': conv_data['last_message'].message,
            'last_message_time': conv_data['last_message'].created_at.isoformat(),
            'unread_count': unread_count,
            'photo_url': photo_url
        })
    
    # Sort by last message time (newest first)
    result.sort(key=lambda x: x['last_message_time'], reverse=True)
    
    return result
