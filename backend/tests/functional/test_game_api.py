from .. import log


def test_create_game(client):
    player1 = client.post(
        "/api/register",
        json={
            "name": "John Doe",
            "email": "test1@example.com",
            "password": "password123",
            "new_player": False
        },
    )
    player2 = client.post(
        "/api/register",
        json={
            "name": "John Doe",
            "email": "test2@example.com",
            "password": "password123",
            "new_player": False
        },
    )
    data_player1 = player1.get_json()
    data_player2 = player2.get_json()
    log.info(data_player1)
    log.info(data_player2)
    response = client.post(
        "/api/game",
        json={
            "player1_id": data_player1["data"]["id"],
            "player2_id": data_player2["data"]["id"],
        },
    )
    json_data = response.get_json()
    log.debug(f'Created game with ID: {json_data["data"]}')
    assert response.status_code == 201


def test_create_play(client):
    play = client.post(
        "/api/game/1/plays",
        json={"type_id": 1, "game_id": 1},
    )
    json_data = play.get_json()
    log.debug(json_data)
    assert play.status_code == 201


def test_list_plays(client):
    plays = client.get("/api/game/1/plays")
    json_data = plays.get_json()
    log.debug(json_data)
    assert plays.status_code == 200


def test_list_multiple_plays(client):
    client.post(
        "/api/game/1/plays",
        json={"type_id": 1, "game_id": 1},
    )
    plays = client.get("/api/game/1/plays")
    json_data = plays.get_json()
    log.debug(json_data)
    assert plays.status_code == 200
    assert json_data["data"]["count"] == 3


def test_insert_play_event(client):
    insert1 = client.post(
        "/api/game/1/play/1",
        json={
            "play_id": "1",
            "player_id": 1,
            "event_type": "score",
            "ball_number": 4
        },
    )
    json_data = insert1.get_json()
    log.debug(json_data)
    insert2 = client.post(
        "/api/game/1/play/1",
        json={
            "play_id": "1",
            "player_id": 1,
            "event_type": "fol",
            "ball_number": 4
        },
    )
    json_data = insert2.get_json()
    log.debug(json_data)
    insert3 = client.post(
        "/api/game/1/play/1",
        json={
            "play_id": "1",
            "player_id": 1,
            "event_type": "win",
            "ball_number": 5
        },
    )
    json_data = insert3.get_json()
    log.debug(json_data)
    assert insert1.status_code == 201
    assert insert2.status_code == 201
    assert insert3.status_code == 201


def test_get_play_event(client):
    read = client.get(
        "/api/game/1/play/1"
    )
    json_data = read.get_json()
    log.debug(json_data)
    assert read.status_code == 200


def test_wrong_game(client):
    wrong = client.post(
        "/api/game/3/end",
        json={"winner_id": 1, "score_player1": 4, "score_player2": 2},
    )
    json_data = wrong.get_json()
    log.debug(json_data)
    assert wrong.status_code == 400


def test_end_game(client):
    end = client.post(
        "/api/game/1/end",
        json={"winner_id": 1, "score_player1": 4, "score_player2": 2},
    )
    json_data = end.get_json()
    log.debug(json_data)
    assert end.status_code == 200
