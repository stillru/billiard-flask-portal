from backend.extensions import db


class WinReason(db.Model):
    '''
    Support table for win_reasons
    '''
    id = db.Column(db.Integer, primary_key=True)
    '''String '''
    description = db.Column(db.String(255), nullable=False)
    '''Reasons for winning in billiard play'''
