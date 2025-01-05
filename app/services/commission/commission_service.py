from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List

from app.models.commission_model import Commission
from app.dtos.commission.requests import CreateCommissionDTO, UpdateCommissionDTO


class CommissionService:
    @staticmethod
    async def create_commission(db: Session, salon_id: int, commission_data: CreateCommissionDTO) -> Commission:
        """Create a new commission record"""
        commission = Commission(
            salon_id=salon_id,
            **commission_data.model_dump()
        )
        db.add(commission)
        db.commit()
        db.refresh(commission)
        return commission

    @staticmethod
    async def get_salon_commissions(db: Session, salon_id: int) -> List[Commission]:
        """Get all commissions for a salon"""
        return db.query(Commission).filter(Commission.salon_id == salon_id).all()

    @staticmethod
    async def get_employee_commission(db: Session, salon_id: int, employee_id: int) -> Commission:
        """Get commission for specific employee in a salon"""
        commission = db.query(Commission).filter(
            Commission.salon_id == salon_id,
            Commission.employee_id == employee_id
        ).first()
        if not commission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Commission not found"
            )
        return commission

    @staticmethod
    async def update_commission(
        db: Session, 
        salon_id: int, 
        employee_id: int, 
        commission_data: UpdateCommissionDTO
    ) -> Commission:
        """Update commission for an employee"""
        commission = await CommissionService.get_employee_commission(db, salon_id, employee_id)
        
        for field, value in commission_data.model_dump(exclude_unset=True).items():
            setattr(commission, field, value)
            
        db.commit()
        db.refresh(commission)
        return commission