from dotenv import load_dotenv, find_dotenv
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
import os

# Chargement du .env
load_dotenv(find_dotenv())

# Récupération sécurisée de la DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL.startswith("postgresql+asyncpg"):
    # Autoriser SQLite en environnement CI (GitHub Actions définit toujours CI=true)
    if not (DATABASE_URL.startswith("sqlite") and os.getenv("CI") == "true"):
        raise ValueError(f"Mauvais driver détecté : {DATABASE_URL}")


# Création du moteur asynchrone
engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=False)

# Création du sessionmaker asynchrone
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Dépendance pour FastAPI
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session
