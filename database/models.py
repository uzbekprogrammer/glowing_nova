from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database.core import Base

class UserSubmission(Base):
    __tablename__ = "user_submissions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    region = Column(String, nullable=False)
    district = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<UserSubmission(id={self.id}, user_id={self.user_id}, region='{self.region}')>"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    full_name = Column(String, nullable=True)
    username = Column(String, nullable=True)
    joined_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<User(id={self.id}, telegram_id={self.telegram_id})>"
