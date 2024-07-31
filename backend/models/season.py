from extensions import db


class Season(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    games = db.relationship("Game", backref="season", lazy=True)
    tournaments = db.relationship("Tournament", backref="season", lazy=True)
