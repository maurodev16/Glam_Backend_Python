from sqlalchemy import Column, Integer, String, Text, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base

class OfferingService(Base):
    __tablename__ = "offering_service"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    duration = Column(Numeric, nullable=True)
    price = Column(Numeric, nullable=True)
    salon_id = Column(Integer, ForeignKey("salons.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    category = Column(String(100), nullable=True)
    estimated_duration = Column(Integer, nullable=True)

    salon = relationship("Salon", back_populates="offering_service")
    appointments = relationship("Appointment", back_populates="offering_service")
    
    # Ajuste para resolver o conflito
    employee_services = relationship("EmployeeService", back_populates="offering_service", overlaps="employees")

