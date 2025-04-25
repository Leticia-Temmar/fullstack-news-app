from app.database import SessionLocal
from app.models.auth import User, Scope
from app.core.security import hash_password

db = SessionLocal()

# Liste des scopes à créer
scope_names = ["create_news", "update_news", "delete_news"]
scopes_dict = {}

# Créer les scopes s'ils n'existent pas
for name in scope_names:
    scope = db.query(Scope).filter(Scope.name == name).first()
    if not scope:
        scope = Scope(name=name)
        db.add(scope)
        db.commit()
        db.refresh(scope)
    scopes_dict[name] = scope

# Liste des utilisateurs à créer avec leurs scopes
users_to_create = [
    {
        "email": "test_create@user.com",
        "password": "test1234",
        "scopes": ["create_news"]
    },
    {
        "email": "test_update@user.com",
        "password": "test1234",
        "scopes": ["update_news"]
    },
    {
        "email": "test_delete@user.com",
        "password": "test1234",
        "scopes": ["delete_news"]
    },
    {
        "email": "test_admin@user.com",
        "password": "test1234",
        "scopes": ["create_news", "update_news", "delete_news"]
    },
]

for user_info in users_to_create:
    user = db.query(User).filter(User.email == user_info["email"]).first()
    if not user:
        user = User(
            email=user_info["email"],
            hashed_password=hash_password(user_info["password"])
        )
        for scope_name in user_info["scopes"]:
            user.scopes.append(scopes_dict[scope_name])
        db.add(user)
        db.commit()

db.close()
print("Utilisateurs de test créés avec succès.")
