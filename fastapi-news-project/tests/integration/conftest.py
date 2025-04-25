import pytest_asyncio
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from httpx import ASGITransport, AsyncClient
from app.main import app
from app.database import get_async_session
from app.models.Categorie import Categorie
from app.models.news_model import News
from app.models.auth import Scope, User, UserScopeLink
from app.core.security import hash_password

DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest_asyncio.fixture(scope="module")
async def test_engine():
    engine = create_async_engine(DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield engine
    await engine.dispose()

@pytest_asyncio.fixture(scope="module")
async def test_session(test_engine):
    async_session = sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        # Crée une catégorie partagée
        session.add(Categorie(id=1, name="Catégorie test"))
        await session.commit()
        yield session

@pytest_asyncio.fixture(scope="module")
async def client(test_session):
    async def override_get_session():
        yield test_session

    app.dependency_overrides[get_async_session] = override_get_session

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c

@pytest_asyncio.fixture(scope="module")
async def tokens(client, test_session):
    users = {}
    for scope_name in ["create_news", "update_news", "delete_news"]:
        scope = Scope(name=scope_name)
        user = User(email=f"{scope_name}@mail.com", hashed_password=hash_password("password"))
        test_session.add_all([scope, user])
        await test_session.commit()

        link = UserScopeLink(user_id=user.id, scope_id=scope.id)
        test_session.add(link)
        await test_session.commit()

        response = await client.post("/token", data={"username": f"{scope_name}@mail.com", "password": "password"})
        users[scope_name] = response.json()["access_token"]
    return users

@pytest_asyncio.fixture(scope="module")
async def existing_news(test_session):
    
    result = await test_session.exec(select(Categorie).where(Categorie.id == 1))
    categorie = result.first()

    # Crée une news liée à cette catégorie
    news = News(title="News initiale", content="Contenu initial", categorie_id=categorie.id)
    test_session.add(news)
    await test_session.commit()
    await test_session.refresh(news)
    return news

@pytest_asyncio.fixture(scope="module")
async def category_with_news(test_session):
    # Création de la catégorie
    categorie = Categorie(name="Catégorie pagination")
    test_session.add(categorie)
    await test_session.commit()
    await test_session.refresh(categorie)

    # Création de plusieurs news associées à cette catégorie
    news_items = [
        News(title=f"News {i}", content="Contenu", categorie_id=categorie.id)
        for i in range(1, 7)
    ]
    test_session.add_all(news_items)
    await test_session.commit()

    return categorie

