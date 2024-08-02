from datetime import datetime

from extensions import db


class Play(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(
        db.Integer, db.ForeignKey("game.id"), nullable=False
    )  # Foreign key to Game
    type_id = db.Column(db.Integer, db.ForeignKey("play_type.id"), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    winner_id = db.Column(db.Integer, db.ForeignKey("player.id"), nullable=True)
    win_reason_id = db.Column(db.Integer, db.ForeignKey("win_reason.id"), nullable=True)

    winner = db.relationship("Player", foreign_keys=[winner_id])
    game = db.relationship("Game", back_populates="plays")
    win_reason = db.relationship("WinReason")
    type = db.relationship("PlayType")

    def to_dict(self):
        return {
            "id": self.id,
            "game_type": self.type,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "winner_id": self.winner_id,
            "winner": self.winner,
        }


class PlayEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    play_id = db.Column(db.Integer, db.ForeignKey("play.id"), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey("player.id"), nullable=True)
    event_type = db.Column(db.String(50), nullable=False)
    ball_number = db.Column(db.Integer, nullable=True)
    event_time = db.Column(
        db.DateTime, default=db.func.current_timestamp(), nullable=False
    )
    details = db.Column(db.String(255), nullable=True)

    play = db.relationship("Play", foreign_keys=[play_id])
    player = db.relationship("Player", foreign_keys=[player_id])


class PlayType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=True)
