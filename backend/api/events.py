import requests
from flask import Blueprint, request, jsonify, url_for, current_app

from api.game import create_game

event_bp = Blueprint("event_bp", __name__)

from flask import Blueprint, request, jsonify
from models import Play, PlayEvent, WinReason
from decorators import format_response

event_bp = Blueprint("event_bp", __name__)

API_BASE_URL = "http://localhost:5000/api/"  # Replace with your API base URL


@event_bp.route("/events", methods=["POST"])
@format_response
def manage_event():
    data = request.get_json()

    event_type = data.get("event_type")
    if event_type not in ["start_game", "player_scored", "end_game", "start_play", "update_play", "end_play"]:
        return jsonify({"error": "Invalid event type"}), 400

    with current_app.test_client() as client:
        if event_type == "start_game":
            response = client.post(
                "/api/game",
                json={
                    "player1_id": data.get("player1_id"),
                    "player2_id": data.get("player2_id"),
                },
            )
            if response.status_code != 201:
                return jsonify({"error": "Failed to create game", "results": response.get_json()}), 400
            new_game = response.get_json()
            new_event = {
                "event_type": event_type,
                "results": new_game["data"],
            }
            return jsonify(new_event), 200
        elif event_type == "start_play":
            response = client.post(
                f"/api/game/{data.get('game_id')}/plays",
                json={
                    "type_id": data.get('game_id')
                },
            )
            if response.status_code != 201:
                return jsonify({"error": "Failed to create play", "results": response.get_json()}), 400
            new_play = response.get_json()
            new_event = {
                "event_type": event_type,
                "results": new_play["data"]
            }
            return jsonify(new_event), 200
        elif event_type == "player_scored":
            #TODO: Shold be implemented
            response = client.post(
                f"/game/{data.get('game_id')}/plays/scored",
                json={
                    "player_id": data.get("player_id"),
                    "event_type": event_type,
                    "ball_number": data.get("ball_number"),
                    "details": f"Player {data.get('player_id')} scored ball {data.get('ball_number')}",
                },
            )
            if response.status_code != 201:
                return jsonify({"error": "Failed to record score"}), 400
            new_event = response.get_json()

        elif event_type == "end_party":
            response = client.get(f"/winreasons/{data.get('win_reason_id')}")
            if response.status_code != 200:
                return jsonify({"error": "Invalid win reason"}), 400
            win_reason = response.get_json()

            response = client.put(
                f"/parties/{data.get('party_id')}/end",
                json={
                    "winner_id": data.get("winner_id"),
                    "win_reason_id": data.get("win_reason_id"),
                },
            )
            if response.status_code != 200:
                return jsonify({"error": "Failed to end party"}), 400

            new_event = {
                "party_id": data.get("party_id"),
                "player_id": data.get("winner_id"),
                "event_type": event_type,
                "details": f"Party ended: {win_reason['description']}",
            }

        response = client.post("/events", json=new_event)
        if response.status_code != 201:
            return jsonify({"error": "Failed to create event", "result": response.get_json()}), 400

        return jsonify(response.get_json()), 201


def to_dict(self):
    return {
        "id": self.id,
        "party_id": self.party_id,
        "player_id": self.player_id,
        "event_type": self.event_type,
        "ball_number": self.ball_number,
        "event_time": self.event_time,
        "details": self.details,
    }


PlayEvent.to_dict = to_dict
