from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.business_schedule_model import Holiday
from app.dtos.business_schedule.business_holiday.requests import CreateHolidayRequestDTO
from app.dtos.business_schedule.business_holiday.responses import CreatedHolidayResponseDTO


class CreateHolidayService:
    @staticmethod
    async def execute(
        db: Session, 
        salon_id: int, 
        holiday_data: CreateHolidayRequestDTO
    ) -> CreatedHolidayResponseDTO:
        # Verifica se já existe feriado na mesma data
        existing_holiday = db.query(Holiday).filter(
            Holiday.salon_id == salon_id,
            Holiday.date == holiday_data.date
        ).first()

        if existing_holiday:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Holiday already exists for this date"
            )

        # Converte horários se o salão não estiver fechado no feriado
        open_time, close_time = None, None
        if not holiday_data.is_closed:
            if not holiday_data.open_time or not holiday_data.close_time:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Open and close times are required when holiday is not closed"
                )

            try:
                open_time = datetime.strptime(holiday_data.open_time, "%H:%M").time()
                close_time = datetime.strptime(holiday_data.close_time, "%H:%M").time()
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid time format. Use HH:MM"
                )

            if close_time <= open_time:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Close time must be after open time"
                )

        # Cria a instância do feriado
        holiday = Holiday(
            salon_id=salon_id,
            date=holiday_data.date,
            is_closed=holiday_data.is_closed,
            open_time=open_time,
            close_time=close_time
        )

        # Salva no banco de dados
        try:
            db.add(holiday)
            db.commit()
            db.refresh(holiday)
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error saving holiday data: " + str(e)
            )

        # Retorna como DTO de resposta
        return CreatedHolidayResponseDTO(
            id=holiday.id,
            date=holiday.date,
            is_closed=holiday.is_closed,
            open_time=holiday.open_time.isoformat() if holiday.open_time else None,
            close_time=holiday.close_time.isoformat() if holiday.close_time else None,
            salon_id=holiday.salon_id
        )
