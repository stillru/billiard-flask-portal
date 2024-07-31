from extensions import db


class Tournament(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    season_id = db.Column(db.Integer, db.ForeignKey("season.id"), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    games = db.relationship("Game", backref="tournament", lazy=True)
