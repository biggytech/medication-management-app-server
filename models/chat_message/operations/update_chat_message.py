from sqlalchemy.orm import Session
from models.chat_message.chat_message import ChatMessage
from models.chat_message.validations import ChatMessageUpdate
from typing import Optional
from services.db.decorators.with_session import with_session


@with_session
def update_chat_message(session: Session, message_id: int, update_data: ChatMessageUpdate) -> Optional[ChatMessage]:
    """
    Update a chat message (typically to mark as read).
    
    Args:
        session: Database session
        message_id: ID of the message to update
        update_data: Update data
        
    Returns:
        Updated ChatMessage object or None if not found
    """
    message = session.query(ChatMessage).filter(ChatMessage.id == message_id).first()
    
    if not message:
        return None
    
    message.is_read = update_data.is_read
    session.commit()
    session.refresh(message)
    
    return message


@with_session
def mark_messages_as_read(session: Session, user1_id: int, user2_id: int, current_user_id: int) -> int:
    """
    Mark all messages in a conversation as read for the current user.
    
    Args:
        session: Database session
        user1_id: First user ID in the conversation
        user2_id: Second user ID in the conversation
        current_user_id: ID of the user marking messages as read
        
    Returns:
        Number of messages updated
    """
    from sqlalchemy import and_, or_
    
    updated_count = session.query(ChatMessage).filter(
        and_(
            or_(
                and_(ChatMessage.sender_id == user1_id, ChatMessage.receiver_id == user2_id),
                and_(ChatMessage.sender_id == user2_id, ChatMessage.receiver_id == user1_id)
            ),
            ChatMessage.receiver_id == current_user_id,
            ChatMessage.is_read == False
        )
    ).update({'is_read': True})
    
    session.commit()
    return updated_count
