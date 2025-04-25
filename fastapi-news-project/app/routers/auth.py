from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.auth import User, Scope, UserScopeLink
from app.database import get_async_session
from app.core.security import verify_password, create_access_token

router = APIRouter()

@router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_async_session)
):
    # Requête avec jointures explicites User -> UserScopeLink -> Scope
    statement = (
        select(User, Scope)
        .join(UserScopeLink, UserScopeLink.user_id == User.id)
        .join(Scope, Scope.id == UserScopeLink.scope_id)
        .where(User.email == form_data.username)
    )
    result = await db.exec(statement)
    rows = result.all()

    # Vérifie si l'utilisateur existe
    if not rows:
        raise HTTPException(status_code=400, detail="Identifiants incorrects")

    user = rows[0][0]  # Récupère l'objet User (premier élément des tuples)
    scopes = [scope.name for _, scope in rows]  # Liste des scopes (2ème élément des tuples)

    # Vérifie le mot de passe
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Identifiants incorrects")

    # Génère le token
    access_token = create_access_token(data={"sub": user.email, "scopes": scopes})

    return {"access_token": access_token, "token_type": "bearer"}