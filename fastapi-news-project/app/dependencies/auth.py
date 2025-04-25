from fastapi import Depends, HTTPException, status
from fastapi.security import SecurityScopes, APIKeyHeader
from jose import JWTError, jwt
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.future import select

from app.core.security import SECRET_KEY, ALGORITHM
from app.models.auth import User
from app.database import get_async_session

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

async def get_current_user(
    security_scopes: SecurityScopes,
    token: str = Depends(api_key_header),
    db: AsyncSession = Depends(get_async_session)
):
    if token is None or not token.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide ou manquant",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = token[len("Bearer "):]

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalide ou expiré",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        token_scopes = payload.get("scopes", [])
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # 🔄 requête asynchrone pour trouver l'utilisateur
    statement = select(User).where(User.email == email)
    result = await db.exec(statement)
    user = result.first()

    if not user:
        raise credentials_exception

    for scope in security_scopes.scopes:
        if scope not in token_scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission manquante : {scope}",
            )

    return user