from pydantic import BaseModel, Field

class CreateCategoryDTO(BaseModel):
    """DTO para criação de categoria"""
    name: str = Field(..., min_length=1, max_length=100)

    class Config:
        from_attributes = True


class UpdateCategoryDTO(BaseModel):
    """DTO para atualização de categoria"""
    name: str = Field(..., min_length=1, max_length=100)

    class Config:
        from_attributes = True
