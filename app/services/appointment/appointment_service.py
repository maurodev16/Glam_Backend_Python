from sqlalchemy.orm import Session
from app.models.appointment_model import Appointment
from app.dtos.appointment.requests import AppointmentCreateDTO, AppointmentUpdateDTO
from app.dtos.user.responses import UserResponseDTO
from fastapi import HTTPException, status
from datetime import datetime

class AppointmentService:
    @staticmethod
    async def create(db: Session, appointment_data: AppointmentCreateDTO, current_user: UserResponseDTO) -> Appointment:
        """
        Create a new appointment
        """
        try:
            # Verifica se o usuário tem permissão para criar o agendamento
            if not current_user.is_active:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="User does not have permission to create an appointment."
                )

            # Criação do objeto de agendamento
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

            # Adiciona ao banco de dados
            db.add(appointment)
            db.commit()
            db.refresh(appointment)

            return appointment

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error creating appointment: {str(e)}"
            )

    @staticmethod
    async def update(db: Session, appointment_id: int, update_data: AppointmentUpdateDTO, current_user: UserResponseDTO) -> Appointment:
        """
        Update an existing appointment
        """
        appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()

        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Appointment not found"
            )

        # Permissões: somente o usuário que criou o agendamento pode atualizá-lo
        if appointment.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to update this appointment"
            )

        # Atualiza os campos fornecidos
        if update_data.appointment_date:
            appointment.appointment_date = update_data.appointment_date
        if update_data.appointment_time:
            appointment.appointment_time = update_data.appointment_time
        if update_data.status:
            appointment.status = update_data.status

        try:
            db.commit()
            db.refresh(appointment)
            return appointment
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error updating appointment: {str(e)}"
            )

    @staticmethod
    async def get_by_id(db: Session, appointment_id: int, current_user: UserResponseDTO) -> Appointment:
        """
        Retrieve an appointment by its ID
        """
        appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()

        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Appointment not found"
            )

        # Permissão: somente o criador ou um administrador pode visualizar
        if appointment.user_id != current_user.id and not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to view this appointment"
            )

        return appointment

    @staticmethod
    async def delete(db: Session, appointment_id: int, current_user: UserResponseDTO) -> None:
        """
        Delete an appointment
        """
        appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()

        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Appointment not found"
            )

        # Permissão: somente o criador pode excluir
        if appointment.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to delete this appointment"
            )

        try:
            db.delete(appointment)
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error deleting appointment: {str(e)}"
            )
