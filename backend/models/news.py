from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from extensions import db

# Ассоциативная таблица для связи многие-ко-многим между новостями и тегами
news_tags = Table(
    "news_tags",
    db.metadata,
    Column("news_id", Integer, ForeignKey("news.id")),
    Column("tag_id", Integer, ForeignKey("tag.id")),
)


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    source_type = db.Column(db.String(50), nullable=False)
    source_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, title, body, source_type, source_id):
        self.title = title
        self.body = body
        self.source_type = source_type
        self.source_id = source_id

    def __repr__(self):
        return f"<News {self.source_type} - {self.source_id}>"
