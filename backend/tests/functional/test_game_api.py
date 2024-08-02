def test_create_game(client):
    player1 = client.post(
        "/api/register",
        json={
            "name": "John Doe",
            "email": "test1@example.com",
            "password": "password123",
        },
    )
    player2 = client.post(
        "/api/register",
        json={
            "name": "John Doe",
            "email": "test2@example.com",
            "password": "password123",
        },
    )
    print(player1.response())
    print(player2.response())
    response = client.post(
        "/api/games", json={"player1_id": player1.data.id, "player2_id": player2.data.id}
    )
    assert response.status_code == 201
    game_id = response.json["id"]
    print(f"Created game with ID: {game_id}")
