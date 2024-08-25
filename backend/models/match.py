from backend.extensions import db


class Match(db.Model):
    __tablename__ = "matches"

    id = db.Column(db.Integer, primary_key=True)
    round_number = db.Column(
        db.Integer, nullable=True
    )  # Номер раунда, например, 1/16, 1/8 и т.д.
    player1_id = db.Column(db.Integer, db.ForeignKey("players.id"))
    player2_id = db.Column(db.Integer, db.ForeignKey("players.id"))
    winner_id = db.Column(db.Integer, db.ForeignKey("players.id"), nullable=True)
    tournament_id = db.Column(
        db.Integer, db.ForeignKey("tournaments.id"), nullable=True
    )
    match_date = db.Column(db.DateTime(timezone=True), nullable=True)

    # Связь с игроками
    player1 = db.relationship("Player", foreign_keys=[player1_id])
    player2 = db.relationship("Player", foreign_keys=[player2_id])
    winner = db.relationship("Player", foreign_keys=[winner_id])
    tournament = db.relationship("Tournament", back_populates="matches")


Match.games = db.relationship("Game", back_populates="match")
