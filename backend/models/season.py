from backend.extensions import db


class Season(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    games = db.relationship(
        "Game", back_populates="season"
    )  # Changed from backref to back_populates
    tournaments = db.relationship(
        "Tournament", back_populates="season"
    )  # Ensure Tournament also uses back_populates
