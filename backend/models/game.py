from datetime import datetime

from backend.extensions import db


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player1_id = db.Column(db.Integer, db.ForeignKey("player.id"), nullable=False)
    player2_id = db.Column(db.Integer, db.ForeignKey("player.id"), nullable=False)
    score_player1 = db.Column(db.Integer, nullable=True)
    score_player2 = db.Column(db.Integer, nullable=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey("tournament.id"), nullable=True)
    season_id = db.Column(db.Integer, db.ForeignKey("season.id"), nullable=True)
    is_finished = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    ended_at = db.Column(db.DateTime, nullable=True)
    winner_id = db.Column(db.Integer, db.ForeignKey("player.id"), nullable=True)
    plays = db.relationship("Play", back_populates="game", cascade="all, delete-orphan")

    player1 = db.relationship("Player", foreign_keys=[player1_id])
    player2 = db.relationship("Player", foreign_keys=[player2_id])
    tournament = db.relationship("Tournament", back_populates="games")
    season = db.relationship("Season", back_populates="games")

    def to_dict(self):
        return {
            "id": self.id,
            "start_time": self.created_at,
            "end_time": self.ended_at,
            "winner_id": self.winner_id,
            "player1_score": self.score_player1,
            "player2_score": self.score_player2,
            "played_plays": [play.to_dict() for play in self.plays],
        }
