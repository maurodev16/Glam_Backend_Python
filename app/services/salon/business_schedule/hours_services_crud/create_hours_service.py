# app/services/business_hours/create_service.py
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.business_schedule_model import BusinessDay, BusinessHours, DayOfWeek
from app.dtos.business_schedule.business_hours.requests import CreateBusinessHoursRequestDTO
from app.dtos.business_schedule.business_hours.responses import CreatedBusinessHoursResponseDTO
from app.services.salon.business_schedule.validators import validate_hours, validate_salon_owner
from app.models.user_model import User

class CreateBusinessHoursService:
    @staticmethod
    async def execute(
        db: Session, 
        salon_id: int,
        current_user: User, 
        hours_data: CreateBusinessHoursRequestDTO
    ) -> CreatedBusinessHoursResponseDTO:
        try:
            # Valida se o usuário é proprietário do salão
            await validate_salon_owner(db, salon_id, current_user.id)
            
            # Valida os horários de funcionamento
            await validate_hours(hours_data)
        
            # Garante que todos os dias da semana estejam associados ao salão
            days_of_week = db.query(DayOfWeek).all()
            for day in days_of_week:
                existing_business_day = db.query(BusinessDay).filter(
                    BusinessDay.salon_id == salon_id,
                    BusinessDay.day_of_week_id == day.id
                ).first()

                if not existing_business_day:
                    new_business_day = BusinessDay(
                        salon_id=salon_id,
                        day_of_week_id=day.id
                    )
                    db.add(new_business_day)
            db.commit()

            # Busca o `business_day` correspondente
            business_day = db.query(BusinessDay).filter(
                BusinessDay.day_of_week_id == hours_data.day_of_week_id,
                BusinessDay.salon_id == salon_id
            ).first()

            if not business_day:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Business day not found for this salon"
                )

            # Converte strings de tempo para objetos `time`
            open_time = datetime.strptime(hours_data.open_time, "%H:%M").time()
            close_time = datetime.strptime(hours_data.close_time, "%H:%M").time()

            # Verifica se já existe horário para o dia
            existing_hours = db.query(BusinessHours).filter(
                BusinessHours.business_day_id == business_day.id,
                BusinessHours.salon_id == salon_id
            ).first()

            if existing_hours:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Business hours already exist for this day"
                )

            # Cria os horários
            business_hours = BusinessHours(
                business_day_id=business_day.id,
                salon_id=salon_id,
                open_time=open_time,
                close_time=close_time
            )

            db.add(business_hours)
            db.commit()
            db.refresh(business_hours)

            # Retorna no formato do DTO esperado
            return CreatedBusinessHoursResponseDTO(
                 id=business_hours.id,  # Certifique-se de que 'id' existe no modelo 'BusinessHours'
                 day_of_week_id=business_day.day_of_week_id,  # Use o 'day_of_week_id' do 'business_day'
                 open_time=business_hours.open_time.strftime("%H:%M"),
                 close_time=business_hours.close_time.strftime("%H:%M"),
                 salon_id=business_hours.salon_id
             )
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid time format. Use HH:MM"
            )
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
