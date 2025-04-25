from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.future import select

from app.database import get_async_session
from app.models.Categorie import Categorie
from app.schemas import categorie

router = APIRouter(prefix="/categories", tags=["Catégories"])

@router.get("/", response_model=list[categorie.CategorieOut])
async def get_categories(db: AsyncSession = Depends(get_async_session)):
    statement = select(Categorie)
    result = await db.exec(statement)
    categories = result.scalars().all() 
    return [categorie.CategorieOut.model_validate(cat) for cat in categories]
