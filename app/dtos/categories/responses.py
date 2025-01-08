from pydantic import BaseModel

class CategoryResponseDTO(BaseModel):
    """DTO para resposta de categoria"""
    id: int
    name: str

    class Config:
        from_attributes = True
