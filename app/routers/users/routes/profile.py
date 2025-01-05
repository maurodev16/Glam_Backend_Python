# backend/app/routers/users/routes/profile.py
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, logger
from sqlalchemy.orm import Session

from app.routers.auth.routes.me import update_user
from app.services.user import UserService
from app.services.user.update_service import UpdateUserService
from app.routers.auth.dependencies.dependecies import get_current_user

from ....dtos.user.responses import UserResponseDTO
from ...users.routes import status
from ....core.database import get_db
from ....models import user_model as models
from ....dtos.user.requests import UpdateUserDTO

router = APIRouter()

@router.get("/profile", response_model=UserResponseDTO)
async def get_profile(
    current_user: Annotated[models.User, Depends(get_current_user)]
) -> UserResponseDTO:
    """
    Get current user profile.
    
    Returns:
        UserResponseDTO: Current user profile information
    """
    return current_user

@router.put("/profile", response_model=UserResponseDTO)
async def update_profile(
    profile_data: UpdateUserDTO,
    current_user: Annotated[models.User, Depends(get_current_user)],
    db: Session = Depends(get_db)
) -> UserResponseDTO:
    """
    Update user profile.
    
    Args:
        profile_data: New profile data
        current_user: Currently authenticated user
        db: Database session
        
    Returns:
        UserResponseDTO: Updated user profile
        
    Raises:
        HTTPException: If update fails or validation errors occur
    """
    try:
        updated_user = await UpdateUserService.update_user(
            db=db,
            user_id=current_user.id,
            update_data=profile_data
        )
        return updated_user
    except HTTPException as http_ex:
        # Repassar exceções HTTP do serviço
        raise http_ex
    except Exception as e:
        logger.error(f"Unexpected error updating profile: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update profile"
        )