from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.dtos.categories.requests import CreateCategoryDTO
from app.services.salon.category.validator import validate_category_exists
from app.models.catergories_model import Category

class CreateCategoryService:
    @staticmethod
    def execute(db: Session, category_data: CreateCategoryDTO) -> Category:
        """Cria uma nova categoria"""
        # Usando o validador para verificar se a categoria já existe
        validate_category_exists(db, category_data.name)
        
        try:
            # Criar a nova categoria
            category = Category(name=category_data.name)
            db.add(category)
            db.commit()
            db.refresh(category)
            return category
        except Exception as e:
            db.rollback()  # Reverter em caso de erro
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating category: {str(e)}"
            )
