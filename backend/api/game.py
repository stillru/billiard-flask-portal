from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from backend.decorators import format_response
from backend.extensions import db
from backend.models import Match
from backend.schemas.match import MatchSchema
import logging

log = logging.getLogger(__name__)
game_bp = Blueprint("game_bp", __name__)


@game_bp.route("/game")
class HandleGame(MethodView):
    @format_response
    def post(self):
        json_data = request.json
        game_schema = MatchSchema(session=db.session)
        log.info(f"POST /game")
        try:
            new_game = game_schema.load(json_data)
        except ValidationError as err:
            abort(500, message=f"Validation Error: {err}")
        try:
            db.session.add(new_game)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            abort(500, message=f"IntegrityError: {str(e.orig)}")
        all_match = Match.query.all()
        games_schema = MatchSchema(session=db.session, many=True)
        log.debug(f"All games: {games_schema.dump(all_match)}")
        return game_schema.dump(new_game), 201


@game_bp.route("/game/<int:game_id>/match")
class HandleAllMatch(MethodView):
    @format_response
    def post(self):
        pass

    def get(self):
        pass
