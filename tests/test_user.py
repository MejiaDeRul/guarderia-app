def test_create_user(client):
    response = client.post("/users/", json={
        "name": "Test User",
        "email": "test@example.com"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test User"
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_get_users(client):
    # Crear usuario antes
    client.post("/users/", json={
        "name": "Test2",
        "email": "test2@example.com"
    })
    response = client.get("/users/")
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    assert len(users) >= 1
