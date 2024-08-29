from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
import logging

from backend.decorators import format_response
from backend.extensions import db
from backend.models import Match
from backend.schemas import GameSchema
from backend.schemas.match import MatchSchema
from backend.controllers.game_controller import MatchService

log = logging.getLogger(__name__)
game_bp = Blueprint("game_bp", __name__)


class Services:
    match_schema = MatchSchema(session=db.session)
    matches_schema = MatchSchema(session=db.session, many=True)
    controller = MatchService


@game_bp.route("/game")
class HandleGame(MethodView):
    @format_response
    def post(self):
        json_data = request.json
        game_schema = GameSchema(session=db.session)
        log.info(f"POST /game")
        try:
            log.info(f"Request data: {json_data}")
            new_game = game_schema.load(json_data)
            db.session.add(new_game)
            db.session.commit()
            log.info(f"Game added: {new_game}")
            return game_schema.dump(new_game), 201
        except ValidationError as err:
            log.error(f"Validation error: {err}")
            abort(400, message=f"Validation Error: {err}")
        except IntegrityError as e:
            db.session.rollback()
            log.error(f"IntegrityError: {e.orig}")
            abort(400, message=f"IntegrityError: {str(e.orig)}")
        except Exception as e:
            log.error(f"Unexpected error: {e}")
            abort(500, message="An unexpected error occurred")


@game_bp.route("/game/all")
class HandleAllGame(MethodView):
    @format_response
    def get(self):
        log.info("GET /game/all")
        matches_schema = MatchSchema(session=db.session, many=True)
        all_matches = Match.query.all()
        log.debug(f"All matches: {matches_schema.dump(all_matches)}")
        return matches_schema.dump(all_matches), 200


@game_bp.route("/game/<int:game_id>/match")
class HandleAllMatch(MethodView, Services):
    @format_response
    def post(self, game_id):
        try:
            match_service = MatchService()
            match_id = match_service.start_match(game_id)
            return jsonify({"match_id": str(match_id)}), 201
        except ValueError as e:
            log.error(f"ValueError: {e}")
            return jsonify({"error": str(e)}), 400

    @format_response
    def get(self, game_id):
        log.info(f"GET /game/{game_id}/match")
        all_matches = Match.query.filter_by(game_id=game_id).all()
        log.debug(f"Matches in game {game_id}: {self.matches_schema.dump(all_matches)}")
        for i in all_matches:
            self.controller.get_match_status(
                Services.controller(), game_id=game_id, match_id=i.id
            )
        if not all_matches:
            return (
                jsonify(
                    {"count": 0, "message": f"No current matches in game {game_id}"}
                ),
                404,
            )
        return self.matches_schema.dump(all_matches), 200


@game_bp.route("/game/<int:game_id>/match/<int:match_id>")
class HandleMatch(MethodView, Services):
    @format_response
    def get(self, game_id, match_id):
        try:
            status = self.controller.get_match_status(
                self.controller(), match_id=match_id, game_id=game_id
            )
            log.info(f"Match status: {status}")
            return jsonify(status), 200
        except Exception as e:
            log.error(f"Error retrieving match status: {e}")
            abort(500, message="An unexpected error occurred")
