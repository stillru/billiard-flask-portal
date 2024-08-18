from flask import Blueprint, render_template, request

from utils import route_metadata

common_bp = Blueprint("common_bp", __name__)


@common_bp.route("/")
@route_metadata(name="Home", category="Main")
def index():
    return render_template("home/index.html")
