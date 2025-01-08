from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from app.models.junctions.associations import service_providers
class OfferingService(Base):
    __tablename__ = "offering_services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    duration = Column(Integer, nullable=False)  # Duration in minutes
    salon_id = Column(Integer, ForeignKey("salons.id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    salon = relationship("Salon", back_populates="services")
    providers = relationship(
        "User",
        secondary=service_providers,
        back_populates="services",
        overlaps="available_services"
    )
    employees = relationship("User", secondary="service_providers", back_populates="available_services", viewonly=True)
    appointments = relationship("Appointment", back_populates="service")
    portfolio_items = relationship("PortfolioItem", back_populates="offering_service")
