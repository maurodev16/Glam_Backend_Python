from sqlalchemy import Column, String, Integer, DateTime, Enum, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from app.core.enums.enums import StatusRole

class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    business_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=False)
    cnpj = Column(String, unique=True, nullable=True)  # Identificador empresarial no Brasil
    cpf = Column(String, unique=True, nullable=True)   # Identificador pessoal no Brasil
    address = Column(Text, nullable=True)  # Endereço da empresa
    is_active = Column(Enum(StatusRole), default=StatusRole.ACTIVE)
    is_verified = Column(Boolean, default=False)  # Verifica se o tenant foi aprovado por um admin
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=True)

    # Relacionamento com os salões
    salons = relationship("Salon", back_populates="tenant", cascade="all, delete-orphan")
