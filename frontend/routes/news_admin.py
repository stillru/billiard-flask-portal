from flask import render_template, redirect, url_for, request, Blueprint
from forms import NewsForm

from utils import route_metadata

news_bp = Blueprint("news_bp", __name__)

@news_bp.route("/add_news", methods=["GET", "POST"])
@route_metadata(name="Add news", category="News")
def add_news():
    form = NewsForm()

    if form.validate_on_submit():
        return redirect(url_for('common_bp.index'))  # Перенаправление на страницу успешного добавления новости

    return render_template('add_news.html', form=form)
