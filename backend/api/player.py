from flask import request, jsonify, Blueprint

from models.player import Player, User
from extensions import db

from decorators import format_response

player_bp = Blueprint("api", __name__)


@player_bp.route("/register", methods=["POST"])
@format_response
def register():
    data = request.json
    if not data or not "new_player" in data or not data or not "name" in data or not "email" in data or not "password" in data:
        return jsonify({"error": "Invalid input"}), 400

    existing_user = User.query.filter_by(email=data["email"]).first()
    if existing_user:
        return jsonify({"error": "Player already exists"}), 400

    user = User(name=data["name"], password=data['password'], email=data["email"])
    db.session.add(user)
    db.session.commit()
    if 'new_player' in data:
        player = Player(user_id=user.id, score=0, played_games=0)
        db.session.add(player)
        db.session.commit()
        return jsonify({"message": "Registration successful", "id": user.id, "new_player": "Created"}), 201
    return jsonify({"message": "Registration successful", "id": user.id}), 201
