from .. import log


def test_show_all_matches_in_game(client):
    list = client.get("/api/game/1/match")
    json_data = list.get_json()
    log.info(json_data)
    assert list.status_code == 200


def test_create_match_in_game(client):
    new_game = client.post(
        "api/game/1/match",
        json={
            "round_number": 0,
            "player1_id": 1,
            "player2_id": 2,
            "match_date": "2024-01-01",
        },
    )
    json_data = new_game.get_json()
    log.info(json_data)
    assert new_game.status_code == 201

def test_create_second_failed_match_in_game(client):
    new_game = client.post(
        "api/game/1/match",
        json={
            "round_number": 0,
            "player1_id": 1,
            "player2_id": 2,
            "match_date": "2024-01-01",
        },
    )
    json_data = new_game.get_json()
    log.info(json_data)
    assert new_game.status_code == 400

def test_show_all_matches_in_game_should_be_one_game(client):
    list = client.get("/api/game/1/match")
    json_data = list.get_json()
    log.info(json_data)
    assert list.status_code == 200
