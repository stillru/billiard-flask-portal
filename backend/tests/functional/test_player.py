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
    assert json_data["message"] == "Registration successful"


def test_register_missing_data(client):
    response = client.post(
        "/api/register", json={"name": "John Doe", "email": "john@example.com"}
    )
    json_data = response.get_json()
    print(json_data)
    assert response.status_code == 400
    assert "error" in json_data


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
    assert json_data["error"] == "Player already exists"
