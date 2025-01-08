from fastapi import HTTPException
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.salon_model import Salon
from app.models.user_model import User

class DeleteOfferingSalonService:
    @staticmethod
    async def execute(
        db: Session,
        salon_id: int,
        current_user: User
    ) -> None:
        try:
            salon = db.query(Salon).filter(Salon.id == salon_id).first()
            if not salon:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Salon not found"
                )
                
            if salon.owner_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Only salon owner can delete salon"
                )

            db.delete(salon)
            db.commit()
            
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
