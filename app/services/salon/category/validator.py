from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.catergories_model import Category

def validate_category_exists(db: Session, category_name: str):
    """Verifica se a categoria já existe no banco de dados."""
    existing_category = db.query(Category).filter(Category.name == category_name).first()
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category already exists"
        )

