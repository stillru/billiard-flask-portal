from flask import request, jsonify, Blueprint

from extensions import db
from models import Club
from models import Game
from models import News
from models import Tournament

news_bp = Blueprint("api", __name__)


@news_bp.route("/news")
def get_news():
    news_items = News.query.all()
    news_list = []
    for item in news_items:
        source = None
        if item.source_type == "Club":
            source = Club.query.get(item.source_id)
        elif item.source_type == "Tournament":
            source = Tournament.query.get(item.source_id)
        elif item.source_type == "Game":
            source = Game.query.get(item.source_id)

        news_list.append(
            {
                "id": item.id,
                "source_type": item.source_type,
                "source_name": source.name if source else "Unknown",
                "source_id": item.source_id,
                "tags": [tag.name for tag in item.tags],
            }
        )
    return jsonify(news_list)


@news_bp.route("/news/club", methods=["POST"])
def add_club_news():
    data = request.json
    title = data.get("title")
    body = data.get("body")
    club_id = data.get("club_id")

    if not title or not body or not club_id:
        return jsonify({"error": "Missing required fields"}), 400

    news_item = News(title=title, body=body, source_type="club", source_id=club_id)
    db.session.add(news_item)
    db.session.commit()

    return jsonify({"message": "Club news added successfully"}), 201


@news_bp.route("/news/tournament", methods=["POST"])
def add_tournament_news():
    data = request.json
    title = data.get("title")
    body = data.get("body")
    tournament_id = data.get("tournament_id")

    if not title or not body or not tournament_id:
        return jsonify({"error": "Missing required fields"}), 400

    news_item = News(
        title=title, body=body, source_type="tournament", source_id=tournament_id
    )
    db.session.add(news_item)
    db.session.commit()

    return jsonify({"message": "Tournament news added successfully"}), 201


@news_bp.route("/news/game", methods=["POST"])
def add_game_news():
    data = request.json
    title = data.get("title")
    body = data.get("body")
    match_id = data.get("match_id")

    if not title or not body or not match_id:
        return jsonify({"error": "Missing required fields"}), 400

    news_item = News(title=title, body=body, source_type="match", source_id=match_id)
    db.session.add(news_item)
    db.session.commit()

    return jsonify({"message": "Game news added successfully"}), 201


@news_bp.route("/news/party", methods=["POST"])
def add_party_news():
    data = request.json
    title = data.get("title")
    body = data.get("body")
    party_id = data.get("party_id")

    if not title or not body or not party_id:
        return jsonify({"error": "Missing required fields"}), 400

    news_item = News(title=title, body=body, source_type="match", source_id=party_id)
    db.session.add(news_item)
    db.session.commit()

    return jsonify({"message": "Game party added successfully"}), 201
