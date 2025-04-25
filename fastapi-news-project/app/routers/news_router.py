from fastapi import APIRouter, HTTPException, status, Security, Depends
from app.dependencies.auth import get_current_user
from app.models.auth import User
from app.crud import news_crud
from app.database import get_async_session
from sqlmodel.ext.asyncio.session import AsyncSession

# Imports directs des schémas utilisés
from app.models.news_model import News
from app.schemas.news_schema import NewsCreate, NewsRead, NewsListResponse

router = APIRouter(
    prefix="/news",
    tags=["news"]
)

@router.post("/", response_model=News, status_code=status.HTTP_201_CREATED)
async def create_news(
    news: NewsCreate,
    user: User = Security(get_current_user, scopes=["create_news"]),
    db: AsyncSession = Depends(get_async_session)
):
    news = await news_crud.create_news(news, db)
    await db.commit()
    return news



@router.get("/", summary="This route do ...", response_model=NewsListResponse)
async def read_news_list(
    limit: int = 5,
    offset: int = 0,
    search: str | None = None,
    categorie: str | None = None,
    db: AsyncSession = Depends(get_async_session),
):
    news_list = await news_crud.get_news_list(db, limit=limit, offset=offset, search=search, categorie=categorie)
    total = await news_crud.count_news(db, search=search, categorie=categorie)

    news = []
    for item in news_list:
        news.append(NewsRead(
    id=item.News.id,
    created_at=item.News.created_at,
    categorie_id=item.News.categorie_id,
    title=item.News.title,
    content=item.News.content,
    categorie={
        "id": item.Categorie.id,
        "name": item.Categorie.name
    }
))
        
    return {"news": news, "total": total}

@router.get("/category/{category_id}", response_model=NewsListResponse)
async def read_news_by_category(
    category_id: int,
    limit: int = 5,
    offset: int = 0,
    search: str | None = None,
    db: AsyncSession = Depends(get_async_session)
):
    # Récupération des tuples (News, Categorie)
    news_list = await news_crud.get_news_by_category(db, category_id, limit=limit, offset=offset, search=search)
    total = await news_crud.count_news_by_category(db, category_id, search=search)

    # Construction des NewsRead
    news_pydantic = []
    for item in news_list:
        news_pydantic.append(NewsRead(
            id=item.News.id,
            created_at=item.News.created_at,
            categorie_id=item.News.categorie_id,
            title=item.News.title,
            content=item.News.content,
            categorie={
                "id": item.Categorie.id,
                "name": item.Categorie.name
            }
        ))

    return {"news": news_pydantic, "total": total}


@router.get("/{news_id}", response_model=NewsRead)
async def read_news(
    news_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    news = await news_crud.get_news_by_id(db, news_id)
    if news is None:
        raise HTTPException(status_code=404, detail="L'actualité demandée est introuvable ou a été supprimée.")
    return news


@router.delete("/{news_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_news(
    news_id: int,
    user: User = Security(get_current_user, scopes=["delete_news"]),
    db: AsyncSession = Depends(get_async_session)
):
    await news_crud.delete_news(db, news_id)
    await db.commit()
    return 

@router.put("/{news_id}", response_model=None, status_code=200)
async def update_news(
    news_id: int,
    news: NewsCreate,
    user: User = Security(get_current_user, scopes=["update_news"]),
    db: AsyncSession = Depends(get_async_session)
):
    await news_crud.update_news(db, news_id, news) 
    await db.commit()  

   
