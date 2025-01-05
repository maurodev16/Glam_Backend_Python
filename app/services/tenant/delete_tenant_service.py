from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.tenant_model import Tenant

class DeleteTenantService:
    @staticmethod
    async def delete(db: Session, tenant_id: int) -> None:
        """Delete tenant"""
        tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
        if not tenant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tenant not found"
            )
            
        try:
            db.delete(tenant)
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error deleting tenant"
            )