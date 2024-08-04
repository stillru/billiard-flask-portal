from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from extensions import db
'''
Clubs representation
'''

class Club(db.Model):
    id = Column(Integer, primary_key=True)
    '''Inucue id of the club'''
    name = Column(String(255), nullable=False)
    '''Name of the club'''
    description = Column(Text, nullable=True)
    '''Description of the club'''
    news = relationship(
        "News",
        primaryjoin="and_(foreign(News.source_id) == Club.id, News.source_type == 'Club')",
        backref="club",
    )
    '''
    For sorting news from this club
    '''

    def __repr__(self):
        return f"<Club {self.name}>"
