from pydantic import BaseModel, EmailStr
from typing import Optional

from ..models.user_model import UserRole
# Schema base para o usuário (para criação e login)
class UserBase(BaseModel):
    email: EmailStr
    name: str
    phone: str
    role: Optional[UserRole] = UserRole.CLIENT  # Default é 'client'

# Schema para criação do usuário (inclui a senha)
class UserCreate(UserBase):
    password: str

# Schema para login do usuário
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Schema de resposta para usuário (retorna o ID e os dados básicos)
class User(UserBase):
    id: int

class Config:
    orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
