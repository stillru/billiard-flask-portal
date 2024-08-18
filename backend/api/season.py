from flask import Blueprint, jsonify

from backend.decorators import format_response
from backend.models import Season

season_bp = Blueprint("season_bp", __name__)


@season_bp.route("/seasons", methods=["GET", "POST"])
@format_response
def season_handler():
    seasons = Season.query.all()
    seasons_count = len(seasons)
    return (
        jsonify(
            {"count": seasons_count, "items": [season.to_dict() for season in seasons]}
        ),
        200,
    )
    pass
