from sqlalchemy import Column, Integer, String, ForeignKey, Time, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base
class BusinessHours(Base):
    __tablename__ = "business_hours"
    id = Column(Integer, primary_key=True, index=True)
    salon_id = Column(Integer, ForeignKey("salons.id", ondelete="CASCADE"))
    day_of_week = Column(Integer)  # 0 = Monday, 6 = Sunday
    open_time = Column(Time, nullable=False)
    close_time = Column(Time, nullable=False)
    is_closed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    # Relationship
    salon = relationship("Salon", back_populates="business_hours")
    def __repr__(self):
        return f"<BusinessHours(salon_id={self.salon_id}, day={self.day_of_week}, open={self.open_time}, close={self.close_time})>"