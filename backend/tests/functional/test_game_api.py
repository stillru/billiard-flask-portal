from .. import log

def test_show_alt_matches_in_game(client):
    list = client.get(
        "/api/game/1/match"
    )
    json_data = list.get_json()
    log.info(json_data)
    assert list.status_code == 200