from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class ClientBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    preferences: Optional[str] = None
    allergies: Optional[str] = None

class ClientCreate(ClientBase):
    user_id: int

class ClientUpdate(ClientBase):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    loyalty_points: Optional[int] = None

class Client(ClientBase):
    id: int
    user_id: int
    loyalty_points: int
    created_at: datetime

    class Config:
        orm_mode = True