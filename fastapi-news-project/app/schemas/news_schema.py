from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import List
from .categorie import CategorieOut

class NewsBase(BaseModel):
    title: str
    content: str
    categorie_id: int

    @field_validator("title", "content")
    def not_empty(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("Ne doit pas être vide")
        return v

    @field_validator("categorie_id")
    def id_positive(cls, v):
        if v <= 0:
            raise ValueError("categorie_id doit être positif")
        return v

class NewsCreate(NewsBase):
    pass

class NewsRead(NewsBase):
    id: int
    created_at: datetime | None
    categorie: CategorieOut

    model_config = {"from_attributes": True}

class NewsListResponse(BaseModel):
    news: List[NewsRead]
    total: int

    model_config = {"from_attributes": True}
