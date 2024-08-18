import json
import logging

from flask import request, jsonify, Blueprint

from backend.extensions import db
from backend.models import Club, Game, Tournament, News, Tag
from backend.decorators import format_response

log = logging.getLogger()
news_bp = Blueprint("api", __name__)


@news_bp.route("/tags", methods=["GET", "POST"])
@format_response
def handle_tags():
    if request.method == "GET":
        tags = Tag.query.all()
        tags_list = []
        for tag in tags:
            tags_list.append({
                "id": tag.id,
                "name": tag.name
            })
        log.debug(f"list of tags: {jsonify(tags_list)}")
        return jsonify(tags_list), 200
    if request.method == "POST":
        data = request.get_json()
        log.info(data)
        if 'name' not in data:
            return jsonify({'errors': {'name': 'This field is required.'}}), 400
        exist_tags = Tag.query.filter_by(name=data["name"]).first()
        if exist_tags:
            return jsonify({"errors": "This tag already in system"}), 400
        else:
            new_tag = Tag(
                name=data["name"]
            )
            db.session.add(new_tag)
            db.session.commit()
            return jsonify({"message": "New tag add", "id": new_tag.id}), 201


@news_bp.route("/news", methods=["GET", "POST"])
@format_response
def handle_news():
    if request.method == "GET":
        # Обработка GET-запроса - получение всех новостей
        news_items = News.query.all()
        news_list = []
        for item in news_items:
            news_list.append(
                {
                    "id": item.id,
                    "title": item.title,
                    "body": item.body,
                    "source_type": item.source_type,
                    "source_name": "Unknown",
                    "tags": [tag.name for tag in item.tags],
                    "created_at": item.created_at.isoformat(),  # Форматируем дату в ISO 8601
                }
            )
        log.debug('list of tags: ' + str(jsonify(news_list)))
        return jsonify(news_list), 200

    elif request.method == "POST":
        # Обработка POST-запроса - добавление новой новости
        data = request.get_json()

        # Валидация входных данных
        if not data or not all(k in data for k in ("title", "body", "source_type", "tags")):
            return jsonify({"error": "Invalid input data", "details": data}), 400

        # Создание новой записи News
        news_item = News(
            title=data["title"],
            body=str(data["body"]),
            source_type=data["source_type"],
        )

        if "tags" in data:
            log.debug(data["tags"])
            for tag in data["tags"]:
                cur_tag = Tag.query.filter_by(id=tag).all()
                news_item.tags.extend(cur_tag)

        # Сохранение в БД
        try:
            log.debug("Trying to add news to db...")
            db.session.add(news_item)
            db.session.commit()
        except AttributeError as e:
            return jsonify({"error": "Attribute error", "details": e}), 500
        except Exception as e:
            return jsonify({"error": "General exception", "details": e}), 500
        else:
            log.debug(news_item)
            return jsonify({"message": "News item created successfully", "id": news_item.id}), 201
