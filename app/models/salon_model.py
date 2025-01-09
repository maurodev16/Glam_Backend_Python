from sqlalchemy import Column, String, Integer, Float, Boolean, Text, ForeignKey, DateTime, UniqueConstraint, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from sqlalchemy.dialects.postgresql import UUID
from .junctions.associations import salon_employees
import uuid

from sqlalchemy import Column, String, Integer, Float, Boolean, Text, ForeignKey, DateTime, UniqueConstraint, ForeignKeyConstraint, event
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Salon(Base):
    __tablename__ = "salons"

    tenant_id = Column(UUID(as_uuid=True), ForeignKey('tenants.id'), primary_key=True)
    id = Column(Integer, primary_key=True, index=True)
    is_public = Column(Boolean, default=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    address = Column(String(200), nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    cnpj = Column(String(14), nullable=False)
    zip_code = Column(String, nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    rating = Column(Float, default=0)
    total_ratings = Column(Integer, default=0)
    image_url = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    parent_id = Column(Integer, nullable=True)
    parent_tenant_id = Column(UUID(as_uuid=True), nullable=True)
    is_headquarters = Column(Boolean, default=False)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=True)
    
 
    __table_args__ = (
        UniqueConstraint('id', name='uq_salon_id'),
        UniqueConstraint('tenant_id', 'id', name='uq_salon_tenant_id'),
        ForeignKeyConstraint(
            ['parent_tenant_id', 'parent_id'],
            ['salons.tenant_id', 'salons.id'],
            name='fk_salon_parent'
        ),
    )


    # Relationships
    tenant = relationship("Tenant", back_populates="salons", overlaps="tenant")
    branches = relationship(
    "Salon",
    backref="headquarters",
    remote_side=["tenant_id", "id"],
    foreign_keys=[parent_tenant_id, parent_id]
)

    owner = relationship("User", back_populates="owned_salons")
    services = relationship("OfferingService", back_populates="salon", cascade="all, delete-orphan")
    employees = relationship("User", secondary=salon_employees, back_populates="employed_at")
    appointments = relationship("Appointment", back_populates="salon", cascade="all, delete-orphan")
    business_hours = relationship("BusinessHours", back_populates="salon", cascade="all, delete-orphan")
    business_days = relationship("BusinessDay", back_populates="salon", cascade="all, delete-orphan")
    holidays = relationship("Holiday", back_populates="salon", cascade="all, delete-orphan")
    portfolio_items = relationship("PortfolioItem", back_populates="salon", cascade="all, delete-orphan")
    ratings = relationship("Rating", back_populates="salon", cascade="all, delete-orphan")
    commissions = relationship("Commission", back_populates="salon")