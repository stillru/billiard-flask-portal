import random

from flask import jsonify

from backend.extensions import db
from backend.models import Event, Match, Game
from backend.models.match import MatchStatus
from backend.schemas.match import MatchSchema
from backend.utils import log

class MatchService:
    def start_match(self, game_id):
        # Logic to check if there's an active match
        log.info(f"{__name__} - start creating 'match'")
        match_game = Match.query.filter(Match.game_id == game_id).first()
        if match_game == None:
            log.debug(f"No match - {match_game}")
            game = Game.query.filter(Game.id == game_id).first()
            self._create_match(game_id, match_id=None, game=game)
            return 0
        if self._is_active_match(game_id):
            raise ValueError("Active match exists for this game.")


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
        result = Match.query.filter( Match.status == MatchStatus.IN_PROGRESS, Match.game_id == game_id).first()
        if result is None:
            return False
        else:
            return True
        pass

    def _get_next_match_id(self, game_id):
        # Implement the logic to get the next match ID
        pass

    def _create_match(self, game_id, match_id, game):
        match_schema = MatchSchema()
        new_match = Match(
            game_id=game_id,
            player1=game.player1,
            player2=game.player2
        )
        db.session.add(new_match)
        db.session.commit()

    def _retrieve_match_status(self, game_id, match_id):
        # Implement the logic to retrieve match status
        pass

    def _apply_move(self, match_status, data):
        # Implement the logic to apply a move to the match
        pass

    def _check_match_result(self, match_status):
        # Implement the logic to check the result of the match
        pass
