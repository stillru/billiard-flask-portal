import logging

logger = logging.getLogger(__name__)


def test_register_success(client):
    response = client.post(
        "/api/register",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123",
            "new_player": False
        },
    )
    json_data = response.get_json()
    logger.debug(json_data)
    assert response.status_code == 201
    assert json_data["data"]["message"] == "Registration successful"


def test_register_success_with_player(client):
    response = client.post(
        "/api/register",
        json={
            "name": "John Doe",
            "email": "john876@example.com",
            "password": "password123",
            "new_player": True
        },
    )
    json_data = response.get_json()
    logger.debug(json_data)
    assert response.status_code == 201
    assert json_data["data"]["message"] == "Registration successful"


def test_register_missing_data(client):
    response = client.post(
        "/api/register", json={"name": "John Doe", "email": "john@example.com"}
    )
    json_data = response.get_json()
    logger.debug(json_data)
    assert response.status_code == 400
    assert json_data["data"]["error"] == "Invalid input"


def test_register_duplicate_email(client):
    user1 = client.post(
        "/api/register",
        json={
            "name": "John Doe",
            "email": "john5@example.com",
            "password": "password123",
            "new_player": False
        },
    )
    user2 = client.post(
        "/api/register",
        json={
            "name": "Jane Doe",
            "email": "john5@example.com",
            "password": "password456",
            "new_player": False
        },
    )
    user1_json_data = user1.get_json()
    user2_json_data = user2.get_json()
    logger.debug(user1_json_data)
    logger.debug(user2_json_data)
    assert user1_json_data["status"] == 201
    assert user2_json_data["status"] == 400
    assert user2_json_data["data"]["error"] == "Player already exists"
