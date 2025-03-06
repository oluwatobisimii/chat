from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    contest_id = Column(String, nullable=False)  # Contest ID
    sender_id = Column(String, nullable=False)  # User ID
    username = Column(String, nullable=False)   # Username
    avatar_color_one = Column(String, nullable=True)
    avatar_color_two = Column(String, nullable=True)
    text = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    reply_to = Column(Integer, nullable=True)  # ID of the message being replied to
    reactions = Column(JSON, nullable=True)    # Reactions as JSON