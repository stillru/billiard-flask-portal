from backend.extensions import db


class Player(db.Model):
    __tablename__ = "players"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    score = db.Column(db.Integer, default=0)
    played_games = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", back_populates="player_id")
    tournament_participants = db.relationship(
        "TournamentParticipant", back_populates="player"
    )
