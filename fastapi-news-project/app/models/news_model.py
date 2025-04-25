from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from sqlalchemy.sql import func
from sqlalchemy import Column, DateTime
from datetime import datetime


if TYPE_CHECKING:
    from app.models.Categorie import Categorie

class News(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)
    title: str
    content: str
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    categorie_id: int = Field(foreign_key="categories.id")
    
    categorie: Optional["Categorie"] = Relationship(back_populates="news")
