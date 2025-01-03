from pydantic import BaseModel, EmailStr, constr
from typing import Optional

class RegisterUserDTO(BaseModel):
    name: str
    email: EmailStr
    password:str
    phone: str
    
class LoginDTO(BaseModel):
    email: EmailStr
    password: str