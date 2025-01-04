# app/services/appointment/update_appointment.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.appointment_model import Appointment
from app.dtos.appointment.requests import AppointmentUpdateDTO
from app.dtos.user.responses import UserResponseDTO
from .get_appointment import GetAppointmentService

class UpdateAppointmentService:
    @staticmethod
    async def execute(
        db: Session,
        appointment_id: int,
        update_data: AppointmentUpdateDTO,
        current_user: UserResponseDTO
    ) -> Appointment:
        try:
            appointment = await GetAppointmentService.execute(
                db, appointment_id, current_user
            )
            await UpdateAppointmentService._validate_owner(appointment, current_user)
            return await UpdateAppointmentService._update_appointment(
                db, appointment, update_data
            )
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error updating appointment: {str(e)}"
            )

    @staticmethod
    async def _validate_owner(
        appointment: Appointment,
        current_user: UserResponseDTO
    ):
        if appointment.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to update this appointment"
            )

    @staticmethod
    async def _update_appointment(
        db: Session,
        appointment: Appointment,
        update_data: AppointmentUpdateDTO
    ) -> Appointment:
        for field, value in update_data.model_dump(exclude_unset=True).items():
            setattr(appointment, field, value)
            
        db.commit()
        db.refresh(appointment)
        return appointment
