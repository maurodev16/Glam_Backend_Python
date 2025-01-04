# app/services/appointment/__init__.py
from .create_appointment import CreateAppointmentService
from .update_appointment import UpdateAppointmentService
from .get_appointment import GetAppointmentService
from .delete_appointment import DeleteAppointmentService

class AppointmentService:
    create = CreateAppointmentService.execute
    update = UpdateAppointmentService.execute
    get = GetAppointmentService.execute
    delete = DeleteAppointmentService.execute

__all__ = ['AppointmentService']
