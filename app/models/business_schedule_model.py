# app/models/business_schedule_model.py
from sqlalchemy import Column, Integer, Boolean, Time, Date, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class BusinessDay(Base):
    __tablename__ = "business_days"
    
    id = Column(Integer, primary_key=True)
    salon_id = Column(Integer, ForeignKey("salons.id"), nullable=False)
    day_of_week = Column(Integer, nullable=False)  # 0-6
    is_open = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(datetime.timezone.utc), onupdate=lambda: datetime.now(datetime.timezone.utc))

    # Relationships
    salon = relationship("Salon", back_populates="business_days")
    hours = relationship("BusinessHours", back_populates="business_day", cascade="all, delete-orphan")

class BusinessHours(Base):
    __tablename__ = "business_hours"
    
    id = Column(Integer, primary_key=True)
    business_day_id = Column(Integer, ForeignKey("business_days.id"), nullable=False)
    salon_id = Column(Integer, ForeignKey("salons.id"), nullable=False)
    open_time = Column(Time, nullable=False)
    close_time = Column(Time, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(datetime.timezone.utc), onupdate=lambda: datetime.now(datetime.timezone.utc))
    # Relationships
    business_day = relationship("BusinessDay", back_populates="hours")
    salon = relationship("Salon", back_populates="business_hours")

class Holiday(Base):
    __tablename__ = "holidays"
    
    id = Column(Integer, primary_key=True)
    salon_id = Column(Integer, ForeignKey("salons.id"), nullable=False)
    date = Column(Date, nullable=False)
    description = Column(String, nullable=True)
    is_closed = Column(Boolean, default=True)
    open_time = Column(Time, nullable=True)
    close_time = Column(Time, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(datetime.timezone.utc), onupdate=lambda: datetime.now(datetime.timezone.utc))
    # Relationships
    salon = relationship("Salon", back_populates="holidays")
