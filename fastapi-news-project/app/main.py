from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from app.database import engine
from app.routers import news_router, categorie, auth
from contextlib import asynccontextmanager
from app.models.auth import User, Scope, UserScopeLink
from app.models.news_model import News
from app.models.Categorie import Categorie

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield  # ← point de passage vers le run de FastAPI

app = FastAPI(lifespan=lifespan)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routers
app.include_router(auth.router)
app.include_router(news_router.router)
app.include_router(categorie.router)
