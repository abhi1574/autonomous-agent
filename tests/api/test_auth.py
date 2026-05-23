def test_login_success(client):
    response = client.post("/auth/token", data={
        "username": "admin",
        "password": "admin123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_wrong_password(client):
    response = client.post("/auth/token", data={
        "username": "admin",
        "password": "wrongpassword"
    })
    assert response.status_code == 401

def test_login_wrong_username(client):
    response = client.post("/auth/token", data={
        "username": "wronguser",
        "password": "admin123"
    })
    assert response.status_code == 401

def test_login_missing_fields(client):
    response = client.post("/auth/token", data={})
    assert response.status_code == 422