from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from ..core.database import get_db
from ..models import salon_model as models
from ..schemas import salon_schema as schemas

router = APIRouter(
    prefix="/salons",
    tags=["salons"]
)

# Listar salões com filtros
@router.get("/", response_model=List[schemas.SalonResponse()])
def get_salons(
    skip: int = 0,
    limit: int = 100,
    city: Optional[str] = None,
    state: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Salon)
    
    if city:
        query = query.filter(models.Salon.city == city)
    if state:
        query = query.filter(models.Salon.state == state)
    if search:
        query = query.filter(
            or_(
                models.Salon.name.ilike(f"%{search}%"),
                models.Salon.description.ilike(f"%{search}%")
            )
        )
    
    salons = query.offset(skip).limit(limit).all()
    return salons

# Buscar salão por ID
@router.get("/{salon_id}", response_model=schemas.SalonResponse())
def get_salon(salon_id: int, db: Session = Depends(get_db)):
    try:
     return db.query(models.Salon).filter(models.Salon.id == salon_id).first()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# Criar novo salão
@router.post("/", response_model=schemas.SalonCreate())
def create_salon(salon: schemas.SalonCreate, db: Session = Depends(get_db)):
    db_salon = models.Salon(**salon.model_dump())
    db.add(db_salon)
    try:
        db.commit()
        db.refresh(db_salon)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return db_salon

# Atualizar salão
@router.put("/{salon_id}", response_model=schemas.SalonUpdate())
def update_salon(
    salon_id: int,
    salon_update: schemas.SalonCreate,
    db: Session = Depends(get_db)
):
    db_salon = db.query(models.Salon).filter(models.Salon.id == salon_id).first()
    if db_salon is None:
        raise HTTPException(status_code=404, detail="Salão não encontrado")
    
    for key, value in salon_update.model_dump().items():
        setattr(db_salon, key, value)
    
    try:
        db.commit()
        db.refresh(db_salon)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
    return db_salon

# Deletar salão
@router.delete("/{salon_id}")
def delete_salon(salon_id: int, db: Session = Depends(get_db)):
    db_salon = db.query(models.Salon).filter(models.Salon.id == salon_id).first()
    if db_salon is None:
        raise HTTPException(status_code=404, detail="Salão não encontrado")
    
    try:
        db.delete(db_salon)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
    return {"message": "Salão deletado com sucesso"}

# Avaliar salão
@router.post("/{salon_id}/rate", response_model=schemas.SalonCreate())
def rate_salon(
    salon_id: int,
    rating: int = Query(..., ge=1, le=5),
    db: Session = Depends(get_db)
):
    db_salon = db.query(models.Salon).filter(models.Salon.id == salon_id).first()
    if db_salon is None:
        raise HTTPException(status_code=404, detail="Salão não encontrado")
    
    # Atualiza a média de avaliações
    total_ratings = db_salon.total_ratings or 0
    current_rating = db_salon.rating or 0
    
    new_total = total_ratings + 1
    new_rating = ((current_rating * total_ratings) + rating) / new_total
    
    db_salon.rating = new_rating
    db_salon.total_ratings = new_total
    
    try:
        db.commit()
        db.refresh(db_salon)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
    return db_salon

# Listar salões por cidade
@router.get("/city/{city}", response_model=List[schemas.SalonResponse()])
def get_salons_by_city(
    city: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    salons = db.query(models.Salon)\
        .filter(models.Salon.city == city)\
        .offset(skip)\
        .limit(limit)\
        .all()
    return salons

# Buscar melhores salões (por avaliação)
@router.get("/top-rated/", response_model=List[schemas.SalonResponse()])
def get_top_rated_salons(
    limit: int = 10,
    min_ratings: int = 5,
    db: Session = Depends(get_db)
):
    salons = db.query(models.Salon)\
        .filter(models.Salon.total_ratings >= min_ratings)\
        .order_by(models.Salon.rating.desc())\
        .limit(limit)\
        .all()
    return salons
