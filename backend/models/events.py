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
    match_id = db.Column(
        db.Integer, db.ForeignKey("matches.id", ondelete="CASCADE"), nullable=False
    )
    event_type = db.Column(db.Enum(EventType), nullable=False)
    data = db.Column(db.JSON, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    player_id = db.Column(db.Integer, db.ForeignKey("players.id"), nullable=True)
    description = db.Column(db.Text, nullable=True)

    match = db.relationship("Match", back_populates="events")
    player = db.relationship("Player", backref="event_records")


class GlobalEvent(db.Model):
    __tablename__ = "all_events"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
