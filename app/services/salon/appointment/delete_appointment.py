# app/services/appointment/delete_appointment.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.dtos.user.responses import UserResponseDTO
from .get_appointment import GetAppointmentService

class DeleteAppointmentService:
    @staticmethod
    async def execute(
        db: Session,
        appointment_id: int,
        current_user: UserResponseDTO
    ) -> None:
        try:
            appointment = await GetAppointmentService.execute(
                db, appointment_id, current_user
            )
            await DeleteAppointmentService._validate_owner(appointment, current_user)
            
            db.delete(appointment)
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error deleting appointment: {str(e)}"
            )

    @staticmethod
    async def _validate_owner(appointment, current_user: UserResponseDTO):
        if appointment.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to delete this appointment"
            )
