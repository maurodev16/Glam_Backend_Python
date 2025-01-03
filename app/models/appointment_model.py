from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id", ondelete="CASCADE"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id",ondelete="CASCADE"), nullable=False)
    salon_id = Column(Integer, ForeignKey("salons.id",ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    status = Column(String(20), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    employee = relationship("Employee", back_populates="appointments")  # Nome correto
    client = relationship("Client", back_populates="appointments")
    service = relationship("Service", back_populates="appointments")
    salon = relationship("Salon", back_populates="appointments")
    
    # Add check constraint for status
    __table_args__ = (
        CheckConstraint(
            status.in_(['scheduled', 'completed', 'cancelled']),
            name='valid_status'
        ),
    )
