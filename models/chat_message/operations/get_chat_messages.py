from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from models.chat_message.chat_message import ChatMessage
from typing import List, Optional
from services.db.decorators.with_session import with_session


@with_session
def get_chat_messages(session: Session, user1_id: int, user2_id: int, limit: int = 50, offset: int = 0) -> List[ChatMessage]:
    """
    Get chat messages between two users.
    
    Args:
        session: Database session
        user1_id: First user ID
        user2_id: Second user ID
        limit: Maximum number of messages to return
        offset: Number of messages to skip
        
    Returns:
        List of ChatMessage objects
    """
    messages = session.query(ChatMessage)\
        .filter(
            or_(
                and_(ChatMessage.sender_id == user1_id, ChatMessage.receiver_id == user2_id),
                and_(ChatMessage.sender_id == user2_id, ChatMessage.receiver_id == user1_id)
            )
        )\
        .order_by(ChatMessage.created_at.desc())\
        .limit(limit)\
        .offset(offset)\
        .all()
    
    return messages


@with_session
def get_chat_messages_by_id(session: Session, message_id: int) -> Optional[ChatMessage]:
    """
    Get a specific chat message by ID.
    
    Args:
        session: Database session
        message_id: ID of the message
        
    Returns:
        ChatMessage object or None if not found
    """
    return session.query(ChatMessage).filter(ChatMessage.id == message_id).first()
