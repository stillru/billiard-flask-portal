from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from extensions import db


class Club(db.Model):
    __tablename__ = "clubs"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    news = relationship(
        "News",
        primaryjoin="and_(foreign(News.source_id) == Club.id, News.source_type == 'Club')",
        backref="club",
    )

    def __repr__(self):
        return f"<Club {self.name}>"
