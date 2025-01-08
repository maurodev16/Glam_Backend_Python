from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.catergories_model import Category

class GetCategoryService:
    @staticmethod
    def execute(db: Session, category_id: int) -> Category:
        """Obtém uma categoria pelo ID"""
        category = db.query(Category).filter(Category.id == category_id).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        return category

