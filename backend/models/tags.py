from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from extensions import db


class Tag(db.Model):

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    news = relationship("News", secondary="news_tags", back_populates="tags")
