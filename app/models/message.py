from sqlalchemy import ForeignKey, Text, String
from sqlalchemy.orm import relationship, Mapped, mapped_column, declarative_base
from typing import List


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)

    sessions: Mapped[List["ChatSession"]] = relationship("ChatSession", back_populates="user")
    messages: Mapped[List["Message"]] = relationship("Message", back_populates="user")


class ChatSession(Base):
    __tablename__ = 'chat_sessions'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    user: Mapped["User"] = relationship("User", back_populates="sessions")
    messages: Mapped[List["Message"]] = relationship("Message", back_populates="session")


class Message(Base):
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey('chat_sessions.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=True)
    message: Mapped[str] = mapped_column(Text)
    role: Mapped[str] = mapped_column(String, default="user")
    session: Mapped["ChatSession"] = relationship("ChatSession", back_populates="messages")

    user: Mapped["User"] = relationship("User", back_populates="messages")