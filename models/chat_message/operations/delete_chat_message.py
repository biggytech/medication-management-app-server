from sqlalchemy.orm import Session
from models.chat_message.chat_message import ChatMessage
from typing import Optional
from services.db.decorators.with_session import with_session


@with_session
def delete_chat_message_by_id(session: Session, message_id: int) -> bool:
    """
    Delete a chat message by ID.
    
    Args:
        session: Database session
        message_id: ID of the message to delete
        
    Returns:
        True if message was deleted, False if not found
    """
    message = session.query(ChatMessage).filter(ChatMessage.id == message_id).first()
    
    if not message:
        return False
    
    session.delete(message)
    session.commit()
    return True
