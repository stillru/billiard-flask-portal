from .. import log


def test_event_create_game(client):
    response = client.get(
        "/api/seasons",
    )
    json_data = response.get_json()
    log.debug(f"Season: {json_data}")
    assert response.status_code == 200
