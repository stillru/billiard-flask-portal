def test_create_game(client, init_data):
    player1, player2, party_type, win_reason1, win_reason2 = init_data

    # Create a game
    response = client.post(
        "/api/games", json={"player1_id": player1.id, "player2_id": player2.id}
    )
    assert response.status_code == 201
    game_id = response.json["id"]
    print(f"Created game with ID: {game_id}")