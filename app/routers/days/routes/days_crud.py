from fastapi import APIRouter, Depends, HTTPException, status
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.dtos.business_schedule.business_day.responses import DayOfWeekResponseDTO
from app.dtos.business_schedule.business_day.requests import DayOfWeekRequestDTO
from app.services.salon.business_schedule.days_service_crud.create_day_service import CreateDayOfWeekService

router = APIRouter()

# Router
@router.post("/", response_model=DayOfWeekResponseDTO)
async def create_day_of_week(
    request: DayOfWeekRequestDTO,
    db: Session = Depends(get_db)
):
    return await CreateDayOfWeekService.execute(db, request)