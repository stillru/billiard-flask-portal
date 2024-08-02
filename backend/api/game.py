import datetime

from flask import Blueprint, request, jsonify
from extensions import db
from models import Game, Party
from decorators import format_response

game_bp = Blueprint("game_bp", __name__)


@game_bp.route("/game", methods=["POST"])
@format_response
def create_game():
    data = request.get_json()
    player1_id = data.get("player1_id")
    player2_id = data.get("player2_id")

    new_game = Game(player1_id=player1_id, player2_id=player2_id)
    db.session.add(new_game)
    db.session.commit()
    return jsonify({"message": "Game created", "id": new_game.id}), 201


@game_bp.route("/game/<int:game_id>/plays", methods=["POST"])
@format_response
def add_party(game_id):
    data = request.get_json()
    type_id = data.get("type_id")

    new_party = Party(
        game_id=game_id,
        type_id=type_id,
        win_reason_id="0",
    )
    db.session.add(new_party)
    db.session.commit()
    return jsonify({"message": "New play started", "id": new_party.id}), 201


@game_bp.route("/game/<int:game_id>/plays", methods=["GET"])
@format_response
def get_parties(game_id):
    parties = Party.query.filter_by(game_id=game_id).all()
    games = len(parties)
    return (
        jsonify({"count": games, "items": [party.to_dict() for party in parties]}),
        200,
    )


@game_bp.route("/game/<int:game_id>/end", methods=["POST"])
@format_response
def end_game(game_id):
    data = request.get_json()
    winner_id = data.get("winner_id")
    score_player1 = data.get("score_player1")
    score_player2 = data.get("score_player2")
    game = Game.query.filter_by(id=game_id).first()
    if not game:
        return jsonify({"message": "Wrong game"}), 400
    else:
        game.winner_id = winner_id
        game.score_player1 = score_player1
        game.score_player2 = score_player2
        game.ended_at = datetime.datetime.utcnow()
        db.session.commit()
        for play in game.parties:
            if play.end_time is None:
                play.end_time = datetime.datetime.utcnow()
                db.session.add(play)
                db.session.commit()
                print(jsonify(f"Updated play: {play.game_id} with {play.end_time}"))
        return (
            jsonify({"results": game.to_dict(), "message": "Game ended successfully"}),
            200,
        )


@game_bp.route("/game/<int:game_id>", methods=["DELETE"])
def delete_game(game_id):
    game = Game.query.get_or_404(game_id)
    db.session.delete(game)
    db.session.commit()
    return jsonify(message="Game deleted successfully"), 200


@game_bp.route("/game/<int:game_id>", methods=["GET"])
def get_game(game_id):
    game = Game.query.get_or_404(game_id)
    return jsonify(game.to_dict()), 200
