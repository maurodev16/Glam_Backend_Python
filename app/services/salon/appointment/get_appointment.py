# app/services/appointment/get_appointment.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.appointment_model import Appointment
from app.dtos.user.responses import UserResponseDTO

class GetAppointmentService:
    @staticmethod
    async def execute(
        db: Session,
        appointment_id: int,
        current_user: UserResponseDTO
    ) -> Appointment:
        appointment = await GetAppointmentService._get_appointment(db, appointment_id)
        await GetAppointmentService._validate_permissions(appointment, current_user)
        return appointment

    @staticmethod
    async def _get_appointment(db: Session, appointment_id: int) -> Appointment:
        appointment = db.query(Appointment).filter(
            Appointment.id == appointment_id
        ).first()
        
        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Appointment not found"
            )
        return appointment

    @staticmethod
    async def _validate_permissions(
        appointment: Appointment,
        current_user: UserResponseDTO
    ):
        if appointment.user_id != current_user.id and not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to view this appointment"
            )
