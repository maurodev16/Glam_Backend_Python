from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from app.dtos.salon.responses import SalonListResponseDTO, SalonResponseDTO
from app.dtos.salon.requests import CreateSalonDTO, UpdateSalonDTO
from app.core.database import get_db
from app.core.enums.enums import UserRole
from app.services.salon import RegisterSalonService, SalonService
from app.models import salon_model
from app.routers.auth.dependencies import get_current_user
from app.models.user_model import User

router = APIRouter()

# Create salon endpoint
@router.post("/", response_model=SalonResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_salon(
    salon: CreateSalonDTO,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Change to User model
) -> SalonResponseDTO:
    created_salon = await SalonService.register(db, salon, current_user)
    return SalonResponseDTO.model_validate(created_salon)

# Atualizar salão
@router.put("/{salon_id}", response_model=SalonResponseDTO)
async def update_salon(
    salon_id: int,
    salon_update: UpdateSalonDTO,
    db: Session = Depends(get_db),
    current_user: salon_model.Salon = Depends(get_current_user)
):
    db_salon = db.query(salon_model.Salon).filter(
        salon_model.Salon.id == salon_id,
        salon_model.Salon.tenant_id == current_user.tenant_id  # Garantir que pertence ao tenant
    ).first()
    
    if db_salon is None:
        raise HTTPException(status_code=404, detail="Salão não encontrado")
    
    # Verificar permissão
    if current_user.role not in [UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar salão")

    for key, value in salon_update.model_dump().items():
        setattr(db_salon, key, value)
    
    try:
        db.commit()
        db.refresh(db_salon)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
    return db_salon

# Listar salões (públicos) com filtros
@router.get("/", response_model=List[SalonListResponseDTO])
def get_salons(
    skip: int = 0,
    limit: int = 100,
    city: Optional[str] = None,
    state: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(salon_model.Salon).filter(salon_model.Salon.is_public == True)  # Apenas salões públicos
    if city:
        query = query.filter(salon_model.Salon.city == city)
    if state:
        query = query.filter(salon_model.Salon.state == state)
    if search:
        query = query.filter(
            or_(
                salon_model.Salon.name.ilike(f"%{search}%"),
                salon_model.Salon.description.ilike(f"%{search}%")
            )
        )
    
    salons = query.offset(skip).limit(limit).all()
    return salons

# Buscar salão por ID
@router.get("/{salon_id}", response_model=SalonResponseDTO)
def get_salon(
    salon_id: int, 
    db: Session = Depends(get_db),
    current_user: salon_model.Salon = Depends(get_current_user)  # Adicionar autenticação
):
    salon = db.query(salon_model.Salon).filter(salon_model.Salon.id == salon_id).first()
    if not salon:
        raise HTTPException(status_code=404, detail="Salão não encontrado")

    # Verifica se o usuário tem acesso ao salão
    if not salon.is_public and salon.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=403, detail="Acesso não autorizado")
    
    return salon


# Deletar salão
@router.delete("/{salon_id}")
async def delete_salon(
    salon_id: int, 
    db: Session = Depends(get_db),
    current_user: salon_model.Salon = Depends(get_current_user)
):
    db_salon = db.query(salon_model.Salon).filter(
        salon_model.Salon.id == salon_id,
        salon_model.Salon.tenant_id == current_user.tenant_id
    ).first()
    
    if db_salon is None:
        raise HTTPException(status_code=404, detail="Salão não encontrado")
    
    # Verificar permissão
    if current_user.role not in [UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Sem permissão para deletar salão")

    try:
        db.delete(db_salon)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
    return {"message": "Salão deletado com sucesso"}

# Avaliar salão (público)
@router.post("/{salon_id}/rate", response_model=SalonResponseDTO)
async def rate_salon(
    salon_id: int,
    rating: int = Query(..., ge=1, le=5),
    db: Session = Depends(get_db),
    current_user: salon_model.Salon = Depends(get_current_user)
):
    db_salon = db.query(salon_model.Salon).filter(
        salon_model.Salon.id == salon_id,
        salon_model.Salon.is_public == True  # Apenas salões públicos podem ser avaliados
    ).first()
    
    if db_salon is None:
        raise HTTPException(status_code=404, detail="Salão não encontrado")
    
    # Implementar lógica para evitar avaliações duplicadas
    # ... (você pode adicionar uma tabela de ratings)
    
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

# Listar salões do tenant atual
@router.get("/my-salons/", response_model=List[SalonResponseDTO])
async def get_tenant_salons(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: salon_model.Salon = Depends(get_current_user)
):
    salons = db.query(salon_model.Salon)\
        .filter(salon_model.Salon.tenant_id == current_user.tenant_id)\
        .offset(skip)\
        .limit(limit)\
        .all()
    return salons