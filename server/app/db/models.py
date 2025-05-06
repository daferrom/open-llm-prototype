from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm ***REMOVED***lationship
from datetime import datetime
from .db import Base

class ChatSession(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)  # opcional si quieres usar auth
    created_at = Column(DateTime, default=lambda: datetime.now())

    messages = relationship("Message", back_populates="session")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"))
    role = Column(String)  # "user" o "assistant"
    content = Column(Text)
    timestamp = Column(DateTime, default=lambda: datetime.now())

    session = relationship("ChatSession", back_populates="messages")
