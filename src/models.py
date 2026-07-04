from fastapi import Depends
from typing import Annotated
from pydantic import EmailStr

from src.database import Base
from sqlalchemy import Column, Boolean, String, DateTime, Enum, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class Users(Base):
    __tablename__ = 'users'

    user_id = Column(String, primary_key=True, index=True, unique=True)
    username = Column(String, index=True, unique=True)
    hashed_password = Column(String, nullable=False)
    privacy = Column(Enum("public", "private", "protected", name="privacy-rules"), default="public")

    email_id = Column(String, nullable=False, unique=True)
    role = Column(Enum("user", "admin", "staff-admin", name="user-roles"), default="user")

    first_name = Column(String)
    phone_no = Column(String)
    profile_image_url = Column(String)

    
    password_reset_tokens = relationship(
        "PasswordResetTokens",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    urls = relationship(
        "Urls",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
class PasswordResetTokens(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(String, primary_key=True, index=True, unique=True)
    user_id = Column(String, ForeignKey("users.user_id", ondelete='CASCADE'), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)

    user = relationship(
        "Users",
        back_populates="password_reset_tokens"
    )


class Urls(Base):
    __tablename__ = "urls"
    url_id = Column(String, primary_key=True)
    url = Column(String, nullable=False)
    user_id = Column(String, ForeignKey("users.user_id", ondelete='CASCADE'), nullable=False)
    clicks = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    blocked = Column(Boolean, default=False)

    user = relationship(
        "Users",
        back_populates="urls"
    )