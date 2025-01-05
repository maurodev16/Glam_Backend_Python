from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    salon_id = Column(Integer, ForeignKey("salons.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Add check constraint for rating
    __table_args__ = (
        CheckConstraint(
            'rating >= 1 AND rating <= 5',
            name='valid_rating_range'
        ),
    )

    # Relationships
    user = relationship("User", back_populates="ratings")
    salon = relationship("Salon", back_populates="ratings")