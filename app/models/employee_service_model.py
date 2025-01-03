from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class EmployeeService(Base):
    __tablename__ = "employee_services"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id",ondelete="CASCADE"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id", ondelete="CASCADE"), nullable=False)

    # Relacionamento com employee
    employee = relationship("Employee", back_populates="available_services", overlaps="service")
    
    # Relacionamento com Service
    service = relationship("Service", back_populates="employee_services", overlaps="employees")
