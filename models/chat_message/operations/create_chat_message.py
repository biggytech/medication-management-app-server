from sqlalchemy.orm import Session
from models.chat_message.chat_message import ChatMessage
from models.chat_message.validations import ChatMessageCreate
from models.patient.patient import Patient
from models.doctor.doctor import Doctor
from models.common.enums.patient_request_status import PatientRequestStatus
from services.db.decorators.with_session import with_session


@with_session
def create_chat_message(session: Session, message_data: ChatMessageCreate, sender_id: int) -> ChatMessage:
    """
    Create a new chat message between users.
    Only allows messages between users who have an approved patient-doctor relationship.
    
    Args:
        session: Database session
        message_data: Chat message data
        sender_id: ID of the user sending the message
        
    Returns:
        Created ChatMessage object
        
    Raises:
        ValueError: If there's no approved patient-doctor relationship between the users
    """
    receiver_id = message_data.receiver_id
    
    # Check if there's an approved patient-doctor relationship
    # Get doctors for both users
    sender_doctor = session.query(Doctor).filter(Doctor.user_id == sender_id).first()
    receiver_doctor = session.query(Doctor).filter(Doctor.user_id == receiver_id).first()
    
    # Check for approved patient relationship
    approved_relationship = None
    if sender_doctor and receiver_doctor:
        # Both are doctors - no relationship needed (they can chat)
        pass
    elif sender_doctor:
        # Sender is doctor, receiver is patient
        approved_relationship = session.query(Patient).filter(
            Patient.doctor_id == sender_doctor.id,
            Patient.user_id == receiver_id,
            Patient.status == PatientRequestStatus.approved
        ).first()
    elif receiver_doctor:
        # Sender is patient, receiver is doctor
        approved_relationship = session.query(Patient).filter(
            Patient.doctor_id == receiver_doctor.id,
            Patient.user_id == sender_id,
            Patient.status == PatientRequestStatus.approved
        ).first()
    else:
        # Neither is a doctor - no relationship needed (regular users can chat)
        pass
    
    # If one is a doctor and the other is not, require approved relationship
    if (sender_doctor or receiver_doctor) and not (sender_doctor and receiver_doctor):
        if not approved_relationship:
            raise ValueError("Cannot send message: No approved patient-doctor relationship exists")
    
    chat_message = ChatMessage(
        sender_id=sender_id,
        receiver_id=receiver_id,
        message=message_data.message
    )
    
    session.add(chat_message)
    session.commit()
    session.refresh(chat_message)
    
    return chat_message
