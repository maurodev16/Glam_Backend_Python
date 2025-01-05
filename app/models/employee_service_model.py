from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class EmployeeService(Base):
    __tablename__ = "employee_services"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id",ondelete="CASCADE"), nullable=False)
    offering_service_id = Column(Integer, ForeignKey("offering_service.id", ondelete="CASCADE"), nullable=False)

    # Relacionamento com employee
    employee = relationship("Employee", back_populates="available_services", overlaps="offering_service")
    
    # Relacionamento com offering_service
    offering_service = relationship("OfferingService", back_populates="employee_services", overlaps="employees")
