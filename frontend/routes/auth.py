from flask import Blueprint, render_template, request

from utils import route_metadata

auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route("/register")
@route_metadata(name="Register", category="General")
def register():
    return render_template("register.html")


@auth_bp.route("/login")
@route_metadata(name="Login", category="General")
def login():
    return "Login Page (to be implemented)"


@auth_bp.route("/error")
@route_metadata(name="Error", category="Utils")
def error():
    error_message = request.args.get("message", "An unknown error occurred.")
    return render_template("error.html", error_message=error_message)
