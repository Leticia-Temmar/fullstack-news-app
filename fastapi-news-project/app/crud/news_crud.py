from datetime import datetime
from zoneinfo import ZoneInfo
from sqlmodel import select
from sqlalchemy import func
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.news_model import News
from app.models.Categorie import Categorie
from app.schemas.news_schema import NewsCreate
from fastapi import HTTPException
# Fonction pour créer une actualité
async def create_news(news: NewsCreate, db: AsyncSession):
    query = select(Categorie).where(Categorie.id == news.categorie_id)
    result = await db.exec(query)
    categorie = result.first()

    if not categorie:
        raise HTTPException(status_code=404, detail="Catégorie non trouvée")

    db_news = News(
        title=news.title,
        content=news.content,
        categorie_id=news.categorie_id,
        created_at=datetime.now(ZoneInfo("UTC"))
    )
    db.add(db_news)
    await db.flush()

    return db_news




# Fonction pour récupérer la liste des actualités
async def get_news_list(
    db: AsyncSession,
    limit: int,
    offset: int,
    search: str | None = None,
    categorie: str | None = None,
):
    
    statement = select(News, Categorie).outerjoin(Categorie, News.categorie_id == Categorie.id)

    if categorie and categorie.lower() != "tous":
        statement = statement.where(Categorie.name == categorie)
    
    if search:
        statement = statement.where(News.title.ilike(f"%{search}%"))

    statement = statement.offset(offset).limit(limit)
    result = (await db.exec(statement)).all()
    return result


async def count_news(
    db: AsyncSession,
    search: str | None = None,
    categorie: str | None = None,
):
    statement = select(func.count(News.id)).join(Categorie)

    if categorie and categorie.lower() != "tous":
        statement = statement.where(Categorie.name == categorie)

    if search:
        statement = statement.where(News.title.ilike(f"%{search}%"))

    result = await db.exec(statement)
    count = result.first()
    
    return count or 0


# Fonction pour récupérer les actualités par catégorie
async def get_news_by_category(db: AsyncSession, category_id: int, limit: int, offset: int, search: str | None):
    statement = select(News, Categorie).join(Categorie, News.categorie_id == Categorie.id).where(News.categorie_id == category_id)

    if search:
        statement = statement.where(News.title.contains(search))

    statement = statement.offset(offset).limit(limit)

    result = await db.exec(statement)
    return result.all()

# Fonction pour compter les actualités par catégorie
async def count_news_by_category(db: AsyncSession, category_id: int, search: str | None = None) -> int:
    statement = select(func.count(News.id)).where(News.categorie_id == category_id)

    if search:
        statement = statement.where(News.title.ilike(f"%{search}%"))
    
    res = (await db.exec(statement)).first()

    return res



# Fonction pour récupérer une actualité par ID
async def get_news_by_id(
    db: AsyncSession,
    news_id: int,
):
    statement = select(News).where(News.id == news_id)
    result = await db.exec(statement)
    return result.first()

# Fonction pour mettre à jour une actualité
async def update_news(
    db: AsyncSession,
    news_id: int,
    updated_news: NewsCreate,
):
    statement = select(News).where(News.id == news_id)
    result = await db.exec(statement)
    news = result.one_or_none()

    if news is None:
        raise HTTPException(status_code=404, detail="News not found")
    
    categorie = await db.get(Categorie, updated_news.categorie_id)
    if not categorie:
        raise HTTPException(status_code=404, detail="Catégory not found")

    news.title = updated_news.title
    news.content = updated_news.content
    news.categorie_id = updated_news.categorie_id

    await db.flush()

# Fonction pour supprimer une actualité
async def delete_news(
    db: AsyncSession,
    news_id: int,
):
    statement = select(News).where(News.id == news_id)
    result = await db.exec(statement)
    news = result.one_or_none() # un resultat ou rien 

    if news is None:
        raise HTTPException(status_code=404, detail="L'actualité demandée est introuvable ou a été supprimée.")

    await db.delete(news)
    await db.flush()

