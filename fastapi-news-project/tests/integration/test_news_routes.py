import pytest
from app.models.auth import Scope, User, UserScopeLink
from app.models.Categorie import Categorie
from app.models.news_model import News
from sqlmodel import select
from app.core.security import  hash_password

@pytest.mark.asyncio
async def test_create_news(client, test_session, tokens):
    # 1. Récupère les tokens depuis la fixture
    token_with_scope = tokens["create_news"]
    
    # Crée un token sans le scope "create_news"
    scope_other = Scope(name="other_scope")
    user_other = User(email="other@mail.com", hashed_password=hash_password("password"))
    test_session.add_all([scope_other, user_other])
    await test_session.commit()
    link = UserScopeLink(user_id=user_other.id, scope_id=scope_other.id)
    test_session.add(link)
    await test_session.commit()

    # Récupère le token pour l'utilisateur sans le scope
    response = await client.post("/token", data={"username": "other@mail.com", "password": "password"})
    token_without_scope = response.json()["access_token"]

    headers_with_scope = {"Authorization": f"Bearer {token_with_scope}"}
    headers_without_scope = {"Authorization": f"Bearer {token_without_scope}"}

    # Récupère la catégorie (créée par la fixture)
    result = await test_session.exec(select(Categorie).where(Categorie.id == 1))
    categorie = result.first()

    # 2. Test : Scope invalide
    response = await client.post("/news/", headers=headers_without_scope, json={
        "title": "Titre",
        "content": "Contenu",
        "categorie_id": categorie.id
    })
    assert response.status_code == 403
    assert response.json()["detail"] == "Permission manquante : create_news"

    # 3. Test : Token invalide
    response = await client.post("/news/", headers={"Authorization": "Bearer invalidtoken"}, json={
        "title": "Titre",
        "content": "Contenu",
        "categorie_id": categorie.id
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Token invalide ou expiré"

    # 4. Test : Format invalide
    response = await client.post("/news/", headers=headers_with_scope, json={})
    assert response.status_code == 422

    # 5. Test : Catégorie non trouvée
    response = await client.post("/news/", headers=headers_with_scope, json={
        "title": "Titre",
        "content": "Contenu",
        "categorie_id": 999
    })
    assert response.status_code == 404

    # 6. Cas nominal
    response = await client.post("/news/", headers=headers_with_scope, json={
        "title": "Titre valide",
        "content": "Contenu valide",
        "categorie_id": categorie.id
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Titre valide"
    assert data["content"] == "Contenu valide"
    assert data["categorie_id"] == categorie.id




@pytest.mark.asyncio
async def test_update_news(client, test_session, tokens, existing_news):
    # 1. Vérifie si le scope "create_news" existe déjà
    result = await test_session.exec(select(Scope).where(Scope.name == "create_news"))
    scope_create = result.first()
    if not scope_create:
        scope_create = Scope(name="create_news")
        test_session.add(scope_create)
        await test_session.commit()
        await test_session.refresh(scope_create)

    # Vérifie si l'utilisateur existe déjà
    result = await test_session.exec(select(User).where(User.email == "scopecreate@mail.com"))
    user_create = result.first()
    if not user_create:
        user_create = User(email="scopecreate@mail.com", hashed_password=hash_password("password"))
        test_session.add(user_create)
        await test_session.commit()
        await test_session.refresh(user_create)

    # Vérifie si le lien existe déjà
    result = await test_session.exec(select(UserScopeLink).where(
    UserScopeLink.user_id == user_create.id, UserScopeLink.scope_id == scope_create.id))
    link = result.first()
    if not link:
        link = UserScopeLink(user_id=user_create.id, scope_id=scope_create.id)
        test_session.add(link)
        await test_session.commit()

    # Récupère le token pour create_news
    response = await client.post("/token", data={"username": "scopecreate@mail.com", "password": "password"})
    token_create_only = response.json()["access_token"]
    headers_create_only = {"Authorization": f"Bearer {token_create_only}"}

    # 2. Récupère les infos de la news existante
    news = existing_news
    categorie_id = news.categorie_id

    # 3. Récupère le token avec update_news (via fixture)
    headers_with_scope = {"Authorization": f"Bearer {tokens['update_news']}"}

    # 4. Scope invalide
    response = await client.put(f"/news/{news.id}", headers=headers_create_only, json={
        "title": "Titre MAJ",
        "content": "Contenu MAJ",
        "categorie_id": categorie_id
    })
    assert response.status_code == 403
    assert response.json()["detail"] == "Permission manquante : update_news"

    # 5. Token invalide
    response = await client.put(f"/news/{news.id}", headers={"Authorization": "Bearer fake"}, json={})
    assert response.status_code == 401
    assert response.json()["detail"] == "Token invalide ou expiré"

    # 6. Format invalide
    response = await client.put(f"/news/{news.id}", headers=headers_with_scope, json={})
    assert response.status_code == 422

    # 7. Catégorie non trouvée
    response = await client.put(f"/news/{news.id}", headers=headers_with_scope, json={
        "title": "Nouveau titre",
        "content": "Nouveau contenu",
        "categorie_id": 999
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "Catégory not found"

    # 8. News non trouvée
    response = await client.put("/news/999", headers=headers_with_scope, json={
        "title": "Nouveau titre",
        "content": "Nouveau contenu",
        "categorie_id": categorie_id
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "News not found"

    # 9. Cas nominal
    response = await client.put(f"/news/{news.id}", headers=headers_with_scope, json={
        "title": "Titre mis à jour",
        "content": "Contenu mis à jour",
        "categorie_id": categorie_id
    })
    assert response.status_code == 200
    assert response.text == "null"


@pytest.mark.asyncio
async def test_delete_news(client, test_session, tokens):
    # 1. Prépare une catégorie et une news à supprimer
    categorie = Categorie(name="Catégorie pour delete")
    test_session.add(categorie)
    await test_session.commit()
    await test_session.refresh(categorie)

    news = News(title="News à supprimer", content="Contenu", categorie_id=categorie.id)
    test_session.add(news)
    await test_session.commit()
    await test_session.refresh(news)

    news_id = news.id
    headers_delete = {"Authorization": f"Bearer {tokens['delete_news']}"}

    # 1. Scope invalide
    headers_without_scope = {"Authorization": f"Bearer {tokens['create_news']}"}
    response = await client.delete(f"/news/{news_id}", headers=headers_without_scope)
    assert response.status_code == 403
    assert response.json()["detail"] == "Permission manquante : delete_news"

    # 2a. Token manquant
    response = await client.delete(f"/news/{news_id}")
    assert response.status_code == 401
    assert response.json()["detail"] == "Token invalide ou manquant"

    # 2b. Token invalide
    response = await client.delete(f"/news/{news_id}", headers={"Authorization": "Bearer fake"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Token invalide ou expiré"

    # 3. News non trouvée
    response = await client.delete(f"/news/999", headers=headers_delete)
    assert response.status_code == 404
    assert response.json()["detail"] == "L'actualité demandée est introuvable ou a été supprimée."

    # 4. Cas nominal (suppression réussie)
    response = await client.delete(f"/news/{news_id}", headers=headers_delete)
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_get_news_by_category(client, category_with_news):
    categorie = category_with_news

    # 1. Catégorie non trouvée
    response = await client.get("/news/category/999")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["news"] == []

    # 2. Cas nominal (sans params)
    response = await client.get(f"/news/category/{categorie.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 6
    assert len(data["news"]) == 5  # Par défaut limit=5
    assert data["news"][0]["title"].startswith("News")

    # 3. Pagination : offset=5 (doit renvoyer la 6ème news)
    response = await client.get(f"/news/category/{categorie.id}?limit=5&offset=5")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 6
    assert len(data["news"]) == 1

    # 4. Pagination : offset trop grand
    response = await client.get(f"/news/category/{categorie.id}?limit=5&offset=100")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 6
    assert data["news"] == []

    # 5. Pagination : limit > total
    response = await client.get(f"/news/category/{categorie.id}?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 6
    assert len(data["news"]) == 6

    # 6. Recherche existante (titre contenant "News 1")
    response = await client.get(f"/news/category/{categorie.id}?search=News 1")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1  # Au moins "News 1"

    # 7. Recherche inexistante
    response = await client.get(f"/news/category/{categorie.id}?search=dragon")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["news"] == []
