from .db import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True, index=True)
    password = Column(String)

    conversations = relationship("Conversation", back_populates="user")

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.username"), nullable=False)
    conversation_id = Column(Integer, nullable=False, index=True)
    query = Column(Text, nullable=False)
    response = Column(Text, nullable=False)

    user = relationship("User", back_populates="conversations")