from sqlalchemy.orm import Session
from models.chat_message.chat_message import ChatMessage
from models.chat_message.validations import ChatMessageCreate
from services.db.decorators.with_session import with_session


@with_session
def create_chat_message(session: Session, message_data: ChatMessageCreate, sender_id: int) -> ChatMessage:
    """
    Create a new chat message between users.
    
    Args:
        session: Database session
        message_data: Chat message data
        sender_id: ID of the user sending the message
        
    Returns:
        Created ChatMessage object
    """
    chat_message = ChatMessage(
        sender_id=sender_id,
        receiver_id=message_data.receiver_id,
        message=message_data.message
    )
    
    session.add(chat_message)
    session.commit()
    session.refresh(chat_message)
    
    return chat_message
