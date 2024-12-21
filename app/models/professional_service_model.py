from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class ProfessionalService(Base):
    __tablename__ = "professional_services"

    id = Column(Integer, primary_key=True, index=True)
    professional_id = Column(Integer, ForeignKey("professionals.id",ondelete="CASCADE"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id", ondelete="CASCADE"), nullable=False)

    # Relacionamento com Professional
    professional = relationship("Professional", back_populates="available_services", overlaps="service")
    
    # Relacionamento com Service
    service = relationship("Service", back_populates="professional_services", overlaps="professionals")
