from flask import Blueprint, request, jsonify

event_bp = Blueprint("event_bp", __name__)

from flask import Blueprint, request, jsonify
from extensions import db
from models import Party, PartyEvent, WinReason

event_bp = Blueprint("event_bp", __name__)


@event_bp.route("/events", methods=["POST"])
def manage_event():
    data = request.get_json()

    event_type = data.get("event_type")
    if event_type not in ["start_party", "player_scored", "end_party"]:
        return jsonify({"error": "Invalid event type"}), 400

    if event_type == "start_party":
        new_party = Party(
            player1_id=data.get("player1_id"),
            player2_id=data.get("player2_id"),
            party_type_id=data.get("party_type_id"),
        )
        db.session.add(new_party)
        db.session.commit()
        new_event = PartyEvent(
            party_id=new_party.id, event_type=event_type, details="Party started"
        )
    elif event_type == "player_scored":
        new_event = PartyEvent(
            party_id=data.get("party_id"),
            player_id=data.get("player_id"),
            event_type=event_type,
            ball_number=data.get("ball_number"),
            details=f"Player {data.get('player_id')} scored ball {data.get('ball_number')}",
        )
    elif event_type == "end_party":
        win_reason = WinReason.query.get(data.get("win_reason_id"))
        if not win_reason:
            return jsonify({"error": "Invalid win reason"}), 400

        party = Party.query.get(data.get("party_id"))
        if not party:
            return jsonify({"error": "Invalid party ID"}), 400

        party.winner_id = data.get("winner_id")
        party.win_reason_id = data.get("win_reason_id")
        party.end_time = db.func.current_timestamp()
        db.session.add(party)

        new_event = PartyEvent(
            party_id=data.get("party_id"),
            player_id=data.get("winner_id"),
            event_type=event_type,
            details=f"Party ended: {win_reason.description}",
        )

    db.session.add(new_event)
    db.session.commit()

    return jsonify(new_event.to_dict()), 201


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


PartyEvent.to_dict = to_dict
