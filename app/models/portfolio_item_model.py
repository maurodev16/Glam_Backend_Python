from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base

class PortfolioItem(Base):
    __tablename__ = "portfolio_items"

    id = Column(Integer, primary_key=True, index=True)
    professional_id = Column(Integer, ForeignKey("professionals.id"), nullable=False)
    salon_id = Column(Integer, ForeignKey("salons.id"), nullable=False)
    image_url = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    professional = relationship("Professional", backref="portfolio_items")
    salon = relationship("Salon", back_populates="portfolio_items")
    service = relationship("Service", backref="portfolio_items")