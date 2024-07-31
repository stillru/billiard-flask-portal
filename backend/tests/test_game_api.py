import pytest
from back import app
from extensions import db
from models import Player, Game, Party, PartyType, WinReason

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["WTF_CSRF_ENABLED"] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

@pytest.fixture
def init_data():
    with app.app_context():
        player1 = Player(name="Player 1")
        player2 = Player(name="Player 2")
        db.session.add_all([player1, player2])
        db.session.commit()

        party_type = PartyType(name="Standard")
        win_reason1 = WinReason(description="Player potted the 8 ball in the correct pocket")
        win_reason2 = WinReason(description="Opponent potted the 8 ball in the wrong pocket")
        db.session.add_all([party_type, win_reason1, win_reason2])
        db.session.commit()

        return player1, player2, party_type, win_reason1, win_reason2

def test_create_game(client, init_data):
    player1, player2, party_type, win_reason1, win_reason2 = init_data

    # Create a game
    response = client.post(
        "/games", json={"player1_id": player1.id, "player2_id": player2.id}
    )
    assert response.status_code == 201
    game_id = response.json["id"]

    # Add first party
    response = client.post(
        f"/games/{game_id}/parties",
        json={
            "type_id": party_type.id,
            "winner_id": player1.id,
            "win_reason_id": win_reason1.id,
        },
    )
    assert response.status_code == 201
    party1_id = response.json["id"]

    # Add second party
    response = client.post(
        f"/games/{game_id}/parties",
        json={
            "type_id": party_type.id,
            "winner_id": player2.id,
            "win_reason_id": win_reason2.id,
        },
    )
    assert response.status_code == 201
    party2_id = response.json["id"]

    # Get all parties in the game
    response = client.get(f"/games/{game_id}/parties")
    assert response.status_code == 200
    parties = response.json
    assert len(parties) == 2

    # End the game
    response = client.put(
        f"/games/{game_id}/end",
        json={"winner_id": player1.id, "score_player1": 5, "score_player2": 3},
    )
    assert response.status_code == 200

    # Delete the game
    response = client.delete(f"/games/{game_id}")
    assert response.status_code == 200

    # Check that the game is deleted
    response = client.get(f"/games/{game_id}")
    assert response.status_code == 404
