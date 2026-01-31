"""
Chat Model
Models for messaging and chat functionality.
"""

from datetime import datetime
from typing import Optional, List
from enum import Enum as PyEnum


class ChatRoomType(str, PyEnum):
    """Types of chat rooms."""
    DIRECT = "direct"
    GROUP = "group"
    SUPPORT = "support"


class MessageType(str, PyEnum):
    """Types of messages."""
    TEXT = "text"
    IMAGE = "image"
    FILE = "file"
    SYSTEM = "system"


class MessageStatus(str, PyEnum):
    """Message delivery status."""
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"


class ChatRoom:
    """
    Chat room model for conversations.
    
    Attributes:
        id: Unique room identifier
        room_type: Type of chat room
        participants: List of participant user IDs
        
        # Context
        context_type: Type of context (e.g., "service", "application")
        context_id: ID of related entity
        
        # Settings
        is_active: Whether room is active
        is_muted: Whether notifications are muted
        
        # Last Message
        last_message_at: Timestamp of last message
        last_message_preview: Preview of last message
        
        # Timestamps
        created_at: Room creation timestamp
    """
    
    __tablename__ = "chat_rooms"
    
    id: str = ""
    room_type: ChatRoomType = ChatRoomType.DIRECT
    participants: List[str] = []
    
    # Context
    context_type: Optional[str] = None
    context_id: Optional[str] = None
    
    # Settings
    is_active: bool = True
    
    # Last Message
    last_message_at: Optional[datetime] = None
    last_message_preview: Optional[str] = None
    
    # Timestamps
    created_at: datetime = datetime.utcnow()
    
    def __init__(self, **kwargs):
        self.participants = []
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def __repr__(self) -> str:
        return f"<ChatRoom(id={self.id}, type={self.room_type})>"


class Message:
    """
    Message model for chat messages.
    
    Attributes:
        id: Unique message identifier
        room_id: Chat room ID
        sender_id: Sender user ID
        
        # Content
        message_type: Type of message
        content: Message content
        file_url: URL if file/image message
        
        # Status
        status: Delivery status
        is_edited: Whether message was edited
        is_deleted: Whether message was deleted
        
        # AI Analysis
        scam_warning: Whether AI flagged potential scam
        warning_message: Warning message if flagged
        
        # Timestamps
        created_at: Message timestamp
        edited_at: Edit timestamp if edited
    """
    
    __tablename__ = "messages"
    
    id: str = ""
    room_id: str = ""
    sender_id: str = ""
    
    # Content
    message_type: MessageType = MessageType.TEXT
    content: str = ""
    file_url: Optional[str] = None
    
    # Status
    status: MessageStatus = MessageStatus.SENT
    is_edited: bool = False
    is_deleted: bool = False
    
    # AI Analysis
    scam_warning: bool = False
    warning_message: Optional[str] = None
    
    # Timestamps
    created_at: datetime = datetime.utcnow()
    edited_at: Optional[datetime] = None
    
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def __repr__(self) -> str:
        return f"<Message(id={self.id}, room={self.room_id}, type={self.message_type})>"
    
    @property
    def display_content(self) -> str:
        """Get content for display (handles deleted messages)."""
        if self.is_deleted:
            return "[Message deleted]"
        return self.content
