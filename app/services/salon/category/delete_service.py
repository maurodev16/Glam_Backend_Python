from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.catergories_model import Category

class DeleteCategoryService:
    @staticmethod
    def execute(db: Session, category_id: int):
        """Deleta uma categoria"""
        category = db.query(Category).filter(Category.id == category_id).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        db.delete(category)
        db.commit()
        return {"detail": "Category deleted successfully"}
