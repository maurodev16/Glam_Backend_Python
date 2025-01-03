# app/routers/user/routes/upgrade.py
from fastapi import APIRouter, Depends, HTTPException, logger, status
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.models.user_model import User
from app.services.user.upgrade_service import UpgradeService
from app.dtos.user.requests import UpgradeToBusinessDTO
from app.dtos.user.responses import UpgradeToBusinessResponseDTO
from app.routers.auth.dependencies import get_current_user

router = APIRouter()

@router.post(
    "/upgrade-to-business",
    response_model=UpgradeToBusinessResponseDTO,
    status_code=status.HTTP_200_OK
)
async def upgrade_to_business(
    upgrade_data: UpgradeToBusinessDTO,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        if current_user.role == "business":
            raise HTTPException(
                status_code=400,
                detail="User is already a business account"
            )
        
        response = await UpgradeService.upgrade_to_business(db, current_user.id, upgrade_data)
        return response
        
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Upgrade failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to upgrade account"
        )
