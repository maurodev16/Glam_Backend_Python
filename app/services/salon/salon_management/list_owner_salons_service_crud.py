from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
import logging
from typing import List

from app.models.salon_model import Salon
from app.models.user_model import User
from app.core.enums.enums import StatusRole

logger = logging.getLogger(__name__)

class ListOwnerSalonsService:
    @staticmethod
    async def execute(db: Session, user: User) -> List[Salon]:
        """Get all active salons owned by a user"""
        try:
            return (
                db.query(Salon)
                .filter(
                    Salon.owner_id == user.id,
                    Salon.is_active == StatusRole.active
                )
                .order_by(Salon.created_at.desc())
                .all()
            )
        except SQLAlchemyError as e:
            logger.error(f"Database error retrieving user salons: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error retrieving salons"
            )
