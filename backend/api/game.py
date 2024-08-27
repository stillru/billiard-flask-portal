from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from backend.decorators import format_response
from backend.extensions import db
from backend.models import Match, Game
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
        """
        Endpoint for creating match
        :param game_id: ID игры, к которой относится матч
        :return: JSON с данными созданного матча или сообщение об ошибке
        """
        log.info(f"POST /match/{game_id}/match")
        json_data = request.json

        # Проверка, существует ли игра с переданным game_id
        game = Game.query.get(game_id)
        if not game:
            abort(404, message=f"Game with id {game_id} not found")
        try:
            # Валидация входящих данных
            matches_schema = MatchSchema(session=db.session)
            match_data = matches_schema.load(json_data)

            # Создание нового матча
            new_match = Match(
                game=game,
                round_number=match_data.get("round_number"),
                player1_id=match_data.get("player1_id"),
                player2_id=match_data.get("player2_id"),
                match_date=match_data.get("match_date"),
            )

            # Добавление матча в базу данных
            db.session.add(new_match)
            db.session.commit()

            # Возврат данных о созданном матче
            return matches_schema.dump(new_match), 201

        except IntegrityError as e:
            db.session.rollback()
            log.error(f"IntegrityError: {e}")
            abort(
                400, message=f"Database error, could not create match. Error: {e.orig}"
            )

        except Exception as e:
            db.session.rollback()
            log.error(f"Unexpected error: {e}")
            abort(500, message=f"Unexpected error occured. Error: {e}")

    def get(self, game_id):
        log.info(f"GET /match/{game_id}/match")
        matches_schema = MatchSchema(session=db.session, many=True)
        all_matches = Match.query.filter(Match.id == game_id).all()
        log.debug(f"All matches in match {game_id}: {matches_schema.dump(all_matches)}")
        return matches_schema.dump(all_matches), 200
