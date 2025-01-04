# app/services/appointment/create_appointment.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime

from app.models.appointment_model import Appointment
from app.dtos.appointment.requests import AppointmentCreateDTO
from app.dtos.user.responses import UserResponseDTO

class CreateAppointmentService:
    @staticmethod
    async def execute(
        db: Session, 
        appointment_data: AppointmentCreateDTO, 
        current_user: UserResponseDTO
    ) -> Appointment:
        try:
            await CreateAppointmentService._validate_user(current_user)
            return await CreateAppointmentService._create_appointment(
                db, appointment_data, current_user
            )
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error creating appointment: {str(e)}"
            )

    @staticmethod
    async def _validate_user(current_user: UserResponseDTO):
        if not current_user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User does not have permission to create an appointment."
            )

    @staticmethod
    async def _create_appointment(
        db: Session,
        appointment_data: AppointmentCreateDTO,
        current_user: UserResponseDTO
    ) -> Appointment:
        appointment = Appointment(
            professional_id=appointment_data.professional_id,
            user_id=current_user.id,
            service_id=appointment_data.service_id,
            salon_id=appointment_data.salon_id,
            appointment_date=appointment_data.appointment_date,
            appointment_time=appointment_data.appointment_time,
            status=appointment_data.status,
            created_at=datetime.utcnow()
        )
        
        db.add(appointment)
        db.commit()
        db.refresh(appointment)
        return appointment
