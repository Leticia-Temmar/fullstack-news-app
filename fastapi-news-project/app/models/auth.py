from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

# Table d'association
class UserScopeLink(SQLModel, table=True):
    __tablename__ = "user_scopes"
    user_id: int = Field(foreign_key="users.id", primary_key=True)
    scope_id: int = Field(foreign_key="scopes.id", primary_key=True)

# Modèle Scope
class Scope(SQLModel, table=True):
    __tablename__ = "scopes"
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    name: str = Field(unique=True)
    users: List["User"] = Relationship(back_populates="scopes", link_model=UserScopeLink)

# Modèle User
class User(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    scopes: List["Scope"] = Relationship(back_populates="users", link_model=UserScopeLink)