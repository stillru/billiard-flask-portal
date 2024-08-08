from .. import log


def test_event_create_game(client):
    player1 = client.post(
        "/api/register",
        json={
            "name": "John Doe",
            "email": "test7@example.com",
            "password": "password123",
            "new_player": True,
        },
    )
    player2 = client.post(
        "/api/register",
        json={
            "name": "John Doe",
            "email": "test8@example.com",
            "password": "password123",
            "new_player": True,
        },
    )
    data_player1 = player1.get_json()
    log.debug(data_player1)
    data_player2 = player2.get_json()
    log.debug(data_player2)
    response = client.post(
        "/api/events",
        json={
            "event_type": "start_game",
            "player1_id": data_player1["data"]["id"],
            "player2_id": data_player2["data"]["id"],
        },
    )
    json_data = response.get_json()
    log.debug(f"Event: {json_data}")
    assert response.status_code == 200


def test_event_create_play(client):
    play = client.post(
        "/api/events",
        json={"event_type": "start_play", "type_id": 1, "game_id": 1},
    )
    json_data = play.get_json()
    log.debug(f"Event: {json_data}")
    assert play.status_code == 200


def test_event_player_scored(client):
    scored = client.post(
        "/api/events",
        json={
            "play_id": 1,
            "type_id": 1,
            "game_id": 1,
            "event_type": "player_scored",
            "event_eventtype": "score",
            "player_id": 1,
            "ball_number": 2,
        },
    )
    json_data = scored.get_json()
    log.debug(f"Event: {json_data}")
    assert scored.status_code == 200
