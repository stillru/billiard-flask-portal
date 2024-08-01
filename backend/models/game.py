from datetime import datetime

from extensions import db


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player1_id = db.Column(db.Integer, db.ForeignKey("player.id"), nullable=False)
    player2_id = db.Column(db.Integer, db.ForeignKey("player.id"), nullable=False)
    score_player1 = db.Column(db.Integer, nullable=False)
    score_player2 = db.Column(db.Integer, nullable=False)
    tournament_id = db.Column(db.Integer, db.ForeignKey("tournament.id"), nullable=True)
    season_id = db.Column(db.Integer, db.ForeignKey("season.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    parties = db.relationship("Party", back_populates="game", cascade='all, delete-orphan')

    player1 = db.relationship("Player", foreign_keys=[player1_id])
    player2 = db.relationship("Player", foreign_keys=[player2_id])
    tournament = db.relationship('Tournament', back_populates='games')
    season = db.relationship('Season', back_populates='games')
