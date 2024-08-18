from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from backend.extensions import db

# Ассоциативная таблица для связи многие-ко-многим между новостями и тегами
news_tags = db.Table(
    "news_tags",
    db.metadata,
    db.Column("news_id", db.Integer, db.ForeignKey("news.id")),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id")),
)


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    source_type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tags = db.relationship("Tag", secondary="news_tags", back_populates="news")
