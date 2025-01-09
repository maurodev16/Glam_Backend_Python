from sqlalchemy import Column, ForeignKey, String, Enum, Integer, DateTime, Table, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from app.core.enums.enums import UserRole, StatusRole
from app.models.junctions.associations import salon_employees, service_providers
from app.models.appointment_model import Appointment
from app.models.rating_model import Rating
from app.models.salon_model import Salon
from sqlalchemy.dialects.postgresql import UUID
import uuid
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.CLIENT)
    is_active = Column(Enum(StatusRole), default=StatusRole.ACTIVE)
    bio = Column(Text, nullable=True)
    profile_image = Column(String, nullable=True)
    commission_rate = Column(Integer, nullable=True)  # Percentage
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    tenant = relationship("Tenant", back_populates="users")
    owned_salons = relationship("Salon", back_populates="owner")
    employed_at = relationship("Salon",secondary=salon_employees, back_populates="employees")
    services = relationship(
        "OfferingService",
        secondary=service_providers,
        back_populates="providers",
        overlaps="available_services"
    )
    available_services = relationship(
        "OfferingService",
        secondary=service_providers,
        back_populates="providers",
        overlaps="services"
    )
    commissions = relationship("Commission", back_populates="employee")
    appointments_provided = relationship("Appointment",foreign_keys=[Appointment.provider_id],back_populates="provider" )
    appointments_booked = relationship("Appointment", foreign_keys=[Appointment.client_id], back_populates="client")
    ratings_given = relationship("Rating", back_populates="user", foreign_keys=[Rating.user_id])
    ratings_received = relationship("Rating", back_populates="provider", foreign_keys=[Rating.service_provider_id])
