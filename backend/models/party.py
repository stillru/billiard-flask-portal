from datetime import datetime

from extensions import db


class Party(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(
        db.Integer, db.ForeignKey("game.id"), nullable=False
    )  # Foreign key to Game
    type_id = db.Column(db.Integer, db.ForeignKey("party_type.id"), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    winner_id = db.Column(db.Integer, db.ForeignKey("player.id"), nullable=True)
    win_reason_id = db.Column(db.Integer, db.ForeignKey("win_reason.id"), nullable=True)

    winner = db.relationship("Player", foreign_keys=[winner_id])
    game = db.relationship("Game", back_populates="parties")
    win_reason = db.relationship("WinReason")
    type = db.relationship("PartyType")


class PartyEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    party_id = db.Column(db.Integer, db.ForeignKey("party.id"), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey("player.id"), nullable=True)
    event_type = db.Column(db.String(50), nullable=False)
    ball_number = db.Column(db.Integer, nullable=True)
    event_time = db.Column(
        db.DateTime, default=db.func.current_timestamp(), nullable=False
    )
    details = db.Column(db.String(255), nullable=True)

    party = db.relationship("Party", foreign_keys=[party_id])
    player = db.relationship("Player", foreign_keys=[player_id])


class PartyType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=True)
