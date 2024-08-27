from itertools import count

from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from backend.decorators import format_response
from backend.extensions import db
from backend.models import Match, Game
from backend.schemas import GameSchema
from backend.schemas.match import MatchSchema
from backend.controllers.game_controller import MatchService
import logging

log = logging.getLogger(__name__)
game_bp = Blueprint("game_bp", __name__)


@game_bp.route("/game")
class HandleGame(MethodView):
    #@format_response
    def post(self):
        json_data = request.json
        game_schema = GameSchema(session=db.session)
        log.info(f" POST /game")
        try:
            log.info(json_data)
            new_game = game_schema.load(json_data)
        except ValidationError as err:
            log.error(f"Validation error in {__class__} - {err}")
            abort(500, message=f"Validation Error: {err}")
        try:
            log.info(f"Trying add new_game to db...")
            db.session.add(new_game)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            log.error(f"...Failed")
            abort(500, message=f"IntegrityError: {str(e.orig)}")
        log.debug(game_schema.dump(new_game))
        return game_schema.dump(new_game), 201


@game_bp.route("/game/all")
class HandleAllGame(MethodView):
    @format_response
    def get(self):
        log.info(f"GET /game/all")
        matches_schema = MatchSchema(session=db.session, many=True)
        all_matches = Match.query.all()
        log.debug(f"All matches: {matches_schema.dump(all_matches)}")
        return matches_schema.dump(all_matches), 200


@game_bp.route("/game/<int:game_id>/match")
class HandleAllMatch(MethodView):

    @format_response
    def post(self, game_id):
        try:
            match_service = MatchService()
            match_id = match_service.start_match(game_id)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        return jsonify({"match_id": f"'{match_id}'"}), 201

    @format_response
    def get(self, game_id):
        log.info(f"GET /match/{game_id}/match")
        matches_schema = MatchSchema(session=db.session, many=True)
        all_matches = Match.query.filter(Match.id == game_id).all()
        log.debug(f"All matches in match {game_id}: {matches_schema.dump(all_matches)}")
        if len(all_matches) < 1:
            return jsonify({"count": 0, "message": f"No current matches in game {game_id}"})
        return matches_schema.dump(all_matches), 200
