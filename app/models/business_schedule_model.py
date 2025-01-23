from sqlalchemy import Column, Integer, Boolean, Time, Date, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class DayOfWeek(Base):
    __tablename__ = "days_of_week"
    id = Column(Integer, primary_key=True)
    day_name = Column(String, unique=True, nullable=False)
    
    # Relationships
    business_days = relationship("BusinessDay", back_populates="day_of_week")

class BusinessDay(Base):
    __tablename__ = "business_days"
    id = Column(Integer, primary_key=True)
    salon_id = Column(Integer, ForeignKey("salons.id", ondelete="CASCADE"), nullable=False)
    day_of_week_id = Column(Integer, ForeignKey("days_of_week.id"), nullable=False)
    is_open = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=True)

    # Relationships
    salon = relationship("Salon", back_populates="business_days")
    day_of_week = relationship("DayOfWeek", back_populates="business_days")
    hours = relationship("BusinessHours", back_populates="business_day", cascade="all, delete-orphan")

class BusinessHours(Base):
    __tablename__ = "business_hours"
    id = Column(Integer, primary_key=True)
    salon_id = Column(Integer, ForeignKey("salons.id", ondelete="CASCADE"), nullable=False)
    business_day_id = Column(Integer, ForeignKey("business_days.id", ondelete="CASCADE"), nullable=False)
    open_time = Column(Time, nullable=False)
    close_time = Column(Time, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=True)

    # Relationships
    salon = relationship("Salon", back_populates="business_hours")
    business_day = relationship("BusinessDay", back_populates="hours")

class Holiday(Base):
    __tablename__ = "holidays"
    id = Column(Integer, primary_key=True)
    salon_id = Column(Integer, ForeignKey("salons.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False)
    is_closed = Column(Boolean, default=True)
    open_time = Column(Time, nullable=True)
    close_time = Column(Time, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=True)

    # Relationships
    salon = relationship("Salon", back_populates="holidays")