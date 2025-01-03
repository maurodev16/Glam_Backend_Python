from sqlalchemy import Column, String, Boolean, JSON, ForeignKey, Text, Integer, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    salon_id = Column(Integer, ForeignKey("salons.id", ondelete="CASCADE"))
    specialties = Column(Text, nullable=True)
    commission_rate = Column(String(20), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    is_active = Column(Boolean, default=True)
    working_hours = Column(JSON, default={
        "monday": {"start": "09:00", "end": "17:00"},
        "tuesday": {"start": "09:00", "end": "17:00"},
        "wednesday": {"start": "09:00", "end": "17:00"},
        "thursday": {"start": "09:00", "end": "17:00"},
        "friday": {"start": "09:00", "end": "17:00"},
        "saturday": {"start": "09:00", "end": "13:00"},
        "sunday": None
    })
    bio = Column(Text, nullable=True)
    profile_image = Column(String(255), nullable=True)

    # Relationships with cascade delete
    user = relationship("User", back_populates="employee")
    salon = relationship("Salon", back_populates="employees")
    appointments = relationship("Appointment", back_populates="employee", cascade="all, delete-orphan")
    available_services = relationship("EmployeeService", back_populates="employee", cascade="all, delete-orphan")