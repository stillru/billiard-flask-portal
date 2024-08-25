from enum import Enum as PyEnum

from backend.extensions import db


class EventType(PyEnum):
    BALL_POTTED = "ball_potted"
    FOUL = "foul"
    TURN_END = "turn_end"
    GAME_WIN = "game_win"


class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey("games.id"))
    player_id = db.Column(db.Integer, db.ForeignKey("players.id"))
    event_type = db.Column(db.Enum(EventType))
    ball_number = db.Column(db.Integer, nullable=True)
    is_foul = db.Column(db.Boolean, default=False)
    game = db.relationship("Game")
    player = db.relationship("Player")
    description = db.Column(db.String)


class GlobalEvent(db.Model):
    __tablename__ = "all_events"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)