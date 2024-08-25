from marshmallow import validates, ValidationError
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

from backend.models.game import Game
from backend.models.match import Match


class GameSchema(SQLAlchemySchema):
    class Meta:
        model = Game
        load_instance = True

    id = auto_field(dump_only=True)
    match_id = auto_field(required=True)
    club_id = auto_field(required=True)
    player1_score = auto_field(required=True)
    player2_score = auto_field(required=True)
    winner_id = auto_field(required=False, allow_none=True)  # Allow None for winner_id


    @validates("player1_score")
    def validate_player1_score(self, value):
        if value < 0:
            raise ValidationError("player1_score must be a non-negative integer.")

    @validates("player2_score")
    def validate_player2_score(self, value):
        if value < 0:
            raise ValidationError("player2_score must be a non-negative integer.")

    @validates("winner_id")
    def validate_winner_id(self, value, **kwargs):
        if value is not None:
            match = Match.query.get(self.context["match_id"])
            if not match:
                raise ValidationError("Invalid match_id.")
            if value not in [match.player1_id, match.player2_id]:
                raise ValidationError(
                    "winner_id must be either player1_id or player2_id from the match."
                )
