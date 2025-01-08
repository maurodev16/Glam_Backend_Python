from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.dtos.categories.requests import  UpdateCategoryDTO
from app.models.catergories_model import Category

class UpdateCategoryService:
    @staticmethod
    def execute(db: Session, category_id: int, category_data: UpdateCategoryDTO) -> Category:
        """Atualiza uma categoria existente"""
        category = db.query(Category).filter(Category.id == category_id).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        
        category.name = category_data.name
        db.commit()
        db.refresh(category)
        return category