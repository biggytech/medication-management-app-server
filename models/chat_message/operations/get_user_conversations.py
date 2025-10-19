from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc
from models.chat_message.chat_message import ChatMessage
from models.user.user import User
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
    
    # Calculate unread counts and format results
    result = []
    for other_user_id, conv_data in conversations_dict.items():
        other_user = user_dict.get(other_user_id)
        if not other_user:
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
        
        result.append({
            'other_user_id': other_user_id,
            'other_user_name': other_user.full_name,
            'last_message': conv_data['last_message'].message,
            'last_message_time': conv_data['last_message'].created_at.isoformat(),
            'unread_count': unread_count
        })
    
    # Sort by last message time (newest first)
    result.sort(key=lambda x: x['last_message_time'], reverse=True)
    
    return result
