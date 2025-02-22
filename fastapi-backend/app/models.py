from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base
class User(Base):
    __tablename__ = "users"
    username = Column(String, primary_key=True, index=True)
    password = Column(String)
    conversations = relationship("Conversation", back_populates="user")
    documents = relationship("Document", back_populates="user")  # New relationship

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.username"), nullable=False)
    conversation_id = Column(Integer, nullable=False, index=True)
    query = Column(String, nullable=False)
    response = Column(String, nullable=False)
    user = relationship("User", back_populates="conversations")

# New Document model
class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.username"), nullable=False)
    file_name = Column(String, nullable=False)
    doc_id = Column(String, nullable=False)  # The ID returned by the vector DB

    user = relationship("User", back_populates="documents")



# from sqlalchemy import Column, Integer, String, ForeignKey, Text
# from sqlalchemy.orm import relationship
# from .db import Base

# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     username = Column(String, unique=True, nullable=False, index=True)
#     password = Column(String, nullable=False)
    
#     conversations = relationship("Conversation", back_populates="user")
#     documents = relationship("Document", back_populates="user")

# class Conversation(Base):
#     __tablename__ = "conversations"
#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     conversation_id = Column(Integer, nullable=False, index=True)
#     query = Column(Text, nullable=False)
#     response = Column(Text, nullable=False)
    
#     user = relationship("User", back_populates="conversations")

# class Document(Base):
#     __tablename__ = "documents"
#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     file_name = Column(String, nullable=False)
#     doc_id = Column(String, nullable=False)  # The ID returned by the vector DB
    
#     user = relationship("User", back_populates="documents")