import pytest

@pytest.mark.asyncio
async def test_login_end_to_end(client, test_session):
    # 1. Préparer un utilisateur en DB
    from app.models.auth import User, Scope, UserScopeLink
    from app.core.security import hash_password

    # Crée le scope
    scope = Scope(name="create_news")
    test_session.add(scope)
    await test_session.commit()

    # Crée l'utilisateur avec le scope
    hashed_password = hash_password("validpassword")
    user = User(email="test@mail.com", hashed_password=hashed_password)
    test_session.add(user)
    await test_session.commit()

    # Lien user/scope
    link = UserScopeLink(user_id=user.id, scope_id=scope.id)
    test_session.add(link)
    await test_session.commit()

    # 2. Cas : champs vides
    response = await client.post("/token", data={"username": "", "password": ""})
    assert response.status_code == 400
    assert response.json()["detail"] == "Identifiants incorrects"

    # 3. Cas : email invalide
    response = await client.post("/token", data={"username": "wrong@mail.com", "password": "validpassword"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Identifiants incorrects"

    # 4. Cas : mauvais mot de passe
    response = await client.post("/token", data={"username": "test@mail.com", "password": "wrongpassword"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Identifiants incorrects"

    # 5. Cas : espaces dans les champs
    response = await client.post("/token", data={"username": "    ", "password": "    "})
    assert response.status_code == 400
    assert response.json()["detail"] == "Identifiants incorrects"

    # 6. Cas nominal : connexion réussie
    response = await client.post("/token", data={"username": "test@mail.com", "password": "validpassword"})
    assert response.status_code == 200
    json_data = response.json()
    assert "access_token" in json_data
    assert json_data["token_type"] == "bearer"
