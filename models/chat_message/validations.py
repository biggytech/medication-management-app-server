from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ChatMessageCreate(BaseModel):
    """Validation schema for creating a new chat message"""
    receiver_id: int = Field(..., description="ID of the user receiving the message")
    message: str = Field(..., min_length=1, max_length=2000, description="Message content")


class ChatMessageResponse(BaseModel):
    """Response schema for chat message"""
    id: int
    sender_id: int
    receiver_id: int
    message: str
    created_at: str
    is_read: bool
    sender_name: Optional[str] = None
    receiver_name: Optional[str] = None


class ChatMessageUpdate(BaseModel):
    """Validation schema for updating a chat message (marking as read)"""
    is_read: bool = Field(..., description="Whether the message has been read")


class ChatConversationResponse(BaseModel):
    """Response schema for a conversation between two users"""
    other_user_id: int
    other_user_name: str
    last_message: Optional[str] = None
    last_message_time: Optional[str] = None
    unread_count: int = 0
