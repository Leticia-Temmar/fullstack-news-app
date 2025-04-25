from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.news_model import News

class Categorie(SQLModel, table=True):
    __tablename__ = "categories"
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    name: str = Field(unique=True)
    
    news: List["News"] = Relationship(back_populates="categorie", sa_relationship_kwargs={"cascade": "all, delete-orphan"})