from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user_model import User
from app.dtos.business_schedule.business_holiday.responses import CreatedHolidayResponseDTO
from app.dtos.business_schedule.business_holiday.requests import CreateHolidayRequestDTO
from app.services.salon.business_schedule.holiday_service_crud.create_holiday_service import CreateHolidayService

router = APIRouter()

@router.post("/", response_model=CreatedHolidayResponseDTO)
async def create_holiday(
    salon_id: int,
    request: CreateHolidayRequestDTO,
    db: Session = Depends(get_db)
):
    service = CreateHolidayService()
    return await service.execute(db, salon_id, request)