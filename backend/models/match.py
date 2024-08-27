from enum import Enum as PyEnum

from backend.extensions import db


class MatchStatus(PyEnum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Match(db.Model):
    __tablename__ = "matches"
    id = db.Column(db.Integer, primary_key=True)
    player1_id = db.Column(db.Integer, db.ForeignKey("players.id"))
    player2_id = db.Column(db.Integer, db.ForeignKey("players.id"))
    winner_id = db.Column(db.Integer, db.ForeignKey("players.id"), nullable=True)
    game_id = db.Column(db.Integer, db.ForeignKey("games.id"), nullable=False)
    match_date = db.Column(db.DateTime(timezone=True), nullable=True)
    status = db.Column(db.Enum(MatchStatus), default=MatchStatus.IN_PROGRESS)

    # Связь с игроками и игрой
    player1 = db.relationship("Player", foreign_keys=[player1_id])
    player2 = db.relationship("Player", foreign_keys=[player2_id])
    winner = db.relationship("Player", foreign_keys=[winner_id])
    game = db.relationship("Game", back_populates="matches")
