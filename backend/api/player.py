from flask import request, jsonify, Blueprint

from models.player import Player  # Проверьте путь к модели
from extensions import db

from decorators import format_response

player_bp = Blueprint("api", __name__)


@player_bp.route("/register", methods=["POST"])
@format_response
def register():
    data = request.json
    if not data or not "name" in data or not "email" in data or not "password" in data:
        return jsonify({"error": "Invalid input"}), 400

    existing_player = Player.query.filter_by(email=data["email"]).first()
    if existing_player:
        return jsonify({"error": "Player already exists"}), 400

    player = Player(name=data["name"], email=data["email"])
    player.set_password(data["password"])
    db.session.add(player)
    db.session.commit()
    return jsonify({"message": "Registration successful", "data": {"id": player.id}}), 201
