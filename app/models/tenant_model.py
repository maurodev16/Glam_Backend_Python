from sqlalchemy import Column, String, Integer, DateTime, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base
from app.core.enums.enums import DocumentType

# In Tenant model:
class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    business_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=False)
    document_type = Column(SQLEnum(DocumentType), nullable=False)
    document = Column(String, unique=True, nullable=False)  # CPF ou CNPJ completo
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=True)

    # Relationships
    users = relationship("User", back_populates="tenant")
    salons = relationship("Salon", back_populates="tenant", cascade="all, delete-orphan")
