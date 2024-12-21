from sqlalchemy import Column, String, Integer, Float, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Salon(Base):
    __tablename__ = "salons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    address = Column(String(200), nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    zip_code = Column(String, nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=True)
    rating = Column(Float, default=0)
    total_ratings = Column(Integer, default=0)
    image_url = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    
    # Relationships with cascade delete
    owner = relationship("User", back_populates="owned_salons")
    services = relationship("Service", back_populates="salon", cascade="all, delete-orphan")
    professionals = relationship("Professional", back_populates="salon", cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="salon", cascade="all, delete-orphan")
    business_hours = relationship("BusinessHours", back_populates="salon", cascade="all, delete-orphan")
    portfolio_items = relationship("PortfolioItem", back_populates="salon", cascade="all, delete-orphan")
    ratings = relationship("Rating", back_populates="salon", cascade="all, delete-orphan")