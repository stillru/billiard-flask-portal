import logging

logger = logging.getLogger(__name__)
def test_event_create_game(client):
    player1 = client.post(
        "/api/register",
        json={
            "name": "John Doe",
            "email": "test3@example.com",
            "password": "password123",
        },
    )
    player2 = client.post(
        "/api/register",
        json={
            "name": "John Doe",
            "email": "test4@example.com",
            "password": "password123",
        },
    )
    data_player1 = player1.get_json()
    data_player2 = player2.get_json()
    response = client.post(
        "/api/events",
        json={
            "event_type": "start_game",
            "player1_id": data_player1["data"]["id"],
            "player2_id": data_player2["data"]["id"],
        },
    )
    json_data = response.get_json()
    logger.info(f"Event: {json_data}")
    assert response.status_code == 200


def test_event_create_play(client):
    play = client.post(
        "/api/events",
        json={
            "event_type": "start_play",
            "type_id": 1,
            "game_id": 1
        },
    )
    json_data = play.get_json()
    logger.info(f"Event: {json_data}")
    assert play.status_code == 200


def test_event_player_scored(client):
    scored = client.post(
        "/api/events",
        json={
            "event_type": "player_scored",
            "player_id": 1,
            "ball_number": 2,
            "details": f"Player 1 scored ball 2",
        },
    )
    json_data = scored.get_json()
    logger.info(f"Event: {json_data}")
    assert scored.status_code != 200
