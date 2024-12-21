from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=True)

    # Relationships with cascade delete
    user = relationship("User", back_populates="client")
    appointments = relationship("Appointment", back_populates="client", cascade="all, delete-orphan")
    ratings = relationship("Rating", back_populates="client", cascade="all, delete-orphan")