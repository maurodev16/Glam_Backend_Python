# app/services/employee/delete_service.py
from sqlalchemy.orm import Session
from .get_service import GetEmployeeService

class DeleteEmployeeService:
    @staticmethod
    async def execute(db: Session, employee_id: int) -> None:
        employee = await GetEmployeeService.execute(db, employee_id)
        db.delete(employee)
        db.commit()
