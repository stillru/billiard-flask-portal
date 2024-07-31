from flask import Blueprint, request, jsonify
from extensions import db
from models import Game, Party

game_bp = Blueprint("game_bp", __name__)


@game_bp.route("/games", methods=["POST"])
def create_game():
    data = request.get_json()
    player1_id = data.get("player1_id")
    player2_id = data.get("player2_id")

    new_game = Game(player1_id=player1_id, player2_id=player2_id)
    db.session.add(new_game)
    db.session.commit()
    return jsonify(id=new_game.id), 201


@game_bp.route("/games/<int:game_id>/parties", methods=["POST"])
def add_party(game_id):
    data = request.get_json()
    type_id = data.get("type_id")
    winner_id = data.get("winner_id")
    win_reason_id = data.get("win_reason_id")

    new_party = Party(
        game_id=game_id,
        type_id=type_id,
        winner_id=winner_id,
        win_reason_id=win_reason_id,
    )
    db.session.add(new_party)
    db.session.commit()
    return jsonify(id=new_party.id), 201


@game_bp.route("/games/<int:game_id>/parties", methods=["GET"])
def get_parties(game_id):
    parties = Party.query.filter_by(game_id=game_id).all()
    return jsonify([party.to_dict() for party in parties]), 200


@game_bp.route("/games/<int:game_id>/end", methods=["PUT"])
def end_game(game_id):
    data = request.get_json()
    winner_id = data.get("winner_id")
    score_player1 = data.get("score_player1")
    score_player2 = data.get("score_player2")

    game = Game.query.get_or_404(game_id)
    game.winner_id = winner_id
    game.score_player1 = score_player1
    game.score_player2 = score_player2
    db.session.commit()
    return jsonify(message="Game ended successfully"), 200


@game_bp.route("/games/<int:game_id>", methods=["DELETE"])
def delete_game(game_id):
    game = Game.query.get_or_404(game_id)
    db.session.delete(game)
    db.session.commit()
    return jsonify(message="Game deleted successfully"), 200


@game_bp.route("/games/<int:game_id>", methods=["GET"])
def get_game(game_id):
    game = Game.query.get_or_404(game_id)
    return jsonify(game.to_dict()), 200
