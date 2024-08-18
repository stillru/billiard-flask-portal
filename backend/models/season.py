from backend.extensions import db


class Season(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    games = db.relationship(
        "Game", back_populates="season"
    )  # Changed from backref to back_populates
    tournaments = db.relationship(
        "Tournament", back_populates="season"
    )  # Ensure Tournament also uses back_populates

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "is_active": self.is_active,
            "games": self.games,
            "tounaments": self.tournaments,
        }
