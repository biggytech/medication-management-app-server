from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import String, ForeignKey, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base
from models.user.user import User


@dataclass
class ChatMessage(Base):
    """
    Chat message model for communication between users and doctors.
    Each message belongs to a conversation between a patient and a doctor.
    """
    __tablename__ = "chat_messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    receiver_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    is_read: Mapped[bool] = mapped_column(default=False)
    
    # Relationships
    sender: Mapped["User"] = relationship("User", foreign_keys=[sender_id])
    receiver: Mapped["User"] = relationship("User", foreign_keys=[receiver_id])

    def __repr__(self) -> str:
        return f"ChatMessage(id={self.id!r}, sender_id={self.sender_id!r}, receiver_id={self.receiver_id!r}, message={self.message[:50]}...)"

    def as_dict(self):
        return {
            'id': self.id,
            'sender_id': self.sender_id,
            'receiver_id': self.receiver_id,
            'message': self.message,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_read': self.is_read
        }
