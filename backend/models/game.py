from enum import Enum as PyEnum

from backend.extensions import db


class GameStatus(PyEnum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Game(db.Model):
    __tablename__ = "games"
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey("matches.id"), nullable=True)
    club_id = db.Column(db.Integer, db.ForeignKey("clubs.id"), nullable=True)
    season_id = db.Column(db.Integer, db.ForeignKey("season.id"))
    tournament_id = db.Column(db.Integer, db.ForeignKey("tournaments.id"), nullable=True)
    player1_score = db.Column(db.Integer)
    player2_score = db.Column(db.Integer)
    winner_id = db.Column(db.Integer, db.ForeignKey("players.id"), nullable=True)
    status = db.Column(db.Enum(GameStatus), default=GameStatus.IN_PROGRESS)
    match = db.relationship("Match", back_populates="games")
    club = db.relationship("Club", back_populates="games")
    winner = db.relationship("Player")
    season = db.relationship("Season", back_populates="games")
    tournament = db.relationship("Tournament", back_populates="games")
