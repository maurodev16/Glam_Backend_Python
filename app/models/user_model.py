from sqlalchemy import Column, String, Enum, Integer, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from app.core.enums.enums import UserRole
from app.core.enums.enums import StatusRole

    
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.CLIENT)
    is_active = Column(Enum(StatusRole), default=StatusRole.ACTIVE)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=True)

    # Relationships with cascade delete
    owned_salons = relationship("Salon", back_populates="owner", cascade="all, delete-orphan")
    client = relationship("Client", back_populates="user", cascade="all, delete-orphan", uselist=False)
    professional = relationship("Professional", back_populates="user", cascade="all, delete-orphan", uselist=False)