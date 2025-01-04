from sqlalchemy import Column, Integer, Float, ForeignKey, Enum as SQLEnum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum

from app.core.database import Base

class CommissionType(str, Enum):
    FIXED = "fixed"
    PERCENTAGE = "percentage"

class Commission(Base):
    __tablename__ = "commissions"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    salon_id = Column(Integer, ForeignKey("salons.id"), nullable=False)
    commission_type = Column(SQLEnum(CommissionType), nullable=False)
    value = Column(Float, nullable=False)  # Percentage or fixed amount
    created_at = Column(DateTime, default=lambda: datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(datetime.timezone.utc), onupdate=lambda: datetime.now(datetime.timezone.utc))

    # Relationships
    employee = relationship("User", back_populates="commissions")
    salon = relationship("Salon", back_populates="commissions")