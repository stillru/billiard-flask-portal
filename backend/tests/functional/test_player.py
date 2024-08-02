def test_register_success(client):
    response = client.post(
        "/api/register",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123",
        },
    )
    json_data = response.get_json()
    assert response.status_code == 201
    assert json_data["data"]["message"] == "Registration successful"


def test_register_missing_data(client):
    response = client.post(
        "/api/register", json={"name": "John Doe", "email": "john@example.com"}
    )
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data["data"]["error"] == "Invalid input"


def test_register_duplicate_email(client):
    client.post(
        "/api/register",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123",
        },
    )
    response = client.post(
        "/api/register",
        json={
            "name": "Jane Doe",
            "email": "john@example.com",
            "password": "password456",
        },
    )
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data["data"]["error"] == "Player already exists"
