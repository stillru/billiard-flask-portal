from flask import request, jsonify, current_app
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from backend.decorators import format_response
from backend.models.events import GlobalEvent
from backend.schemas.events import GlobalEventSchema
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from backend.extensions import db
import logging

event_bp = Blueprint("event_bp", __name__)

logger = logging.getLogger(__name__)

class EventService:
    def __init__(self, json_data, client):
        self.json_data = json_data
        self.client = client

    def handle_start_game(self):
        logging.debug("Handle start game event...")
        response = self.client.post(
            "/api/game",
            json={
                "player1_id": self.json_data.get("player1_id"),
                "player2_id": self.json_data.get("player2_id"),
            },
        )
        resp = response.get_json()
        resp["event_type"] = "start_game"
        return resp

    def handle_start_play(self):
        response = self.client.post(
            f"/api/game/{self.json_data.get('game_id')}/plays",
            json={"type_id": self.json_data.get("game_id")},
        )
        resp = response.get_json()
        resp["event_type"] = "start_play"
        return resp

    def handle_player_scored(self):
        response = self.client.post(
            f"/api/game/{self.json_data.get('game_id')}/match/{self.json_data.get('play_id')}",
            json={
                "player_id": self.json_data.get("player_id"),
                "event_type": self.json_data.get("event_eventtype"),
                "ball_number": self.json_data.get("ball_number"),
            },
        )
        return response

    def handle_end_party(self):
        response = self.client.get(f"/winreasons/{self.json_data.get('win_reason_id')}")
        if response.status_code != 200:
            return jsonify({"error": "Invalid win reason"}), 400
        win_reason = response.get_json()

        response = self.client.put(
            f"/parties/{self.json_data.get('party_id')}/end",
            json={
                "winner_id": self.json_data.get("winner_id"),
                "win_reason_id": self.json_data.get("win_reason_id"),
            },
        )
        return response

@event_bp.route("/event")
class Events(MethodView):
    @event_bp.response(200)
    @format_response
    def get(self):
        events = GlobalEvent.query.all()
        events_schema = GlobalEventSchema(many=True)
        return events_schema.dump(events)

    @event_bp.response(201)
    @format_response
    def post(self):
        json_data = request.json
        event_schema = GlobalEventSchema(session=db.session)
        event_type = json_data.get("event_type")
        if event_type not in [
            "start_game",
            "player_scored",
            "end_game",
            "start_play",
            "update_play",
            "end_play",
        ]:
            abort(400, message=f"{event_type} not valid")

        event_service = EventService(json_data, current_app.test_client())

        if event_type == "start_game":
            response_data = event_service.handle_start_game()
        elif event_type == "start_play":
            response = event_service.handle_start_play()
        elif event_type == "player_scored":
            response = event_service.handle_player_scored()
        elif event_type == "end_party":
            response = event_service.handle_end_party()
        else:
            abort(400, message="Unsupported event type")

        if isinstance(response_data, dict):
            try:
                event_new = event_schema.load(response_data)
                db.session.add(event_new)
                db.session.commit()
                logging.debug(event_schema.dump(event_new))
                return event_schema.dump(event_new), 201
            except (ValidationError, IntegrityError) as e:
                db.session.rollback()
                abort(500, message=str(e))
            except Exception as e:
                db.session.rollback()
                abort(500, message=str(e))
        else:
            abort(400, message=response.get_json())