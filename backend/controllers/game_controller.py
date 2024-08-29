from flask_smorest import abort
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from backend.extensions import db
from backend.models import Match, Game
from backend.models.match import MatchStatus
from backend.schemas.match import MatchSchema
from backend.utils import log


class MatchService:
    match_schema = MatchSchema(session=db.session)
    matches_schema = MatchSchema(session=db.session, many=True)

    def start_match(self, game_id):
        # Logic to check if there's an active match
        log.info(f"{__name__} - start creating 'match'")
        match_game = Match.query.filter(Match.game_id == game_id).first()
        if match_game == None:
            log.debug(f"No match - {match_game}")
            game = Game.query.filter(Game.id == game_id).first()
            return self._create_match(game_id, match_id=None, game=game)
        if self._is_active_match(game_id):
            log.debug(f"Yes match - {match_game}")
            return self.match_schema.dump(self._is_active_match(game_id))

        # Logic to get matches and create a new one
        next_match_id = self._get_next_match_id(game_id)
        self._create_match(game_id, next_match_id)
        return next_match_id

    def get_match_status(self, game_id, match_id):
        # Logic to retrieve the match status
        match_status = self._retrieve_match_status(game_id, match_id)
        if match_status is None:
            raise ValueError("Match not found.")
        return match_status

    def update_match_status(self, game_id, match_id, data):
        # Logic to update the match state
        match_status = self._retrieve_match_status(game_id, match_id)
        if match_status is None:
            raise ValueError("Match not found.")

        self._apply_move(match_status, data)
        result = self._check_match_result(match_status)
        return result

    def _is_active_match(self, game_id):
        result = Match.query.filter(
            Match.status == MatchStatus.IN_PROGRESS, Match.game_id == game_id
        ).first()
        if result is None:
            return False
        else:
            return result

    def _get_next_match_id(self, game_id):
        # Implement the logic to get the next match ID
        latest_match = (
            db.session.query(Match)
            .filter(Match.game_id == game_id)
            .order_by(Match.match_id.desc())
            .first()
        )
        next_id = latest_match.id + 1
        return next_id

    def _create_match(self, game_id, match_id, game):
        new_match = Match(game_id=game_id, player1=game.player1, player2=game.player2)
        try:
            log.debug(f"Request data: {new_match}")
            db.session.add(new_match)
            db.session.commit()
            log.debug(f"Match added: {new_match}")
            return self.match_schema.dump(new_match)
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

    def _retrieve_match_status(self, game_id, match_id):
        log.debug(f"Getting status for match in game {game_id} - {match_id}")
        match_schema = MatchSchema(session=db.session)
        match = Match.query.filter(
            Match.id == match_id, Match.game_id == game_id
        ).first()
        return match_schema.dump(match)

    def _apply_move(self, match_status, data):
        # Implement the logic to apply a move to the match
        pass

    def _check_match_result(self, match_status):
        # Implement the logic to check the result of the match
        pass
