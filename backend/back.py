import logging

from flask import Flask
from flask_cors import CORS

from api.player import player_bp
from api.news import news_bp
from api.game import game_bp
from api.events import event_bp
from config import Config, configure_logging
from extensions import db, migrate

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate.init_app(app, db)
CORS(app)

configure_logging()
logger = logging.getLogger(__name__)

app.register_blueprint(player_bp, url_prefix="/api", name="player_api")
app.register_blueprint(news_bp, url_prefix="/api", name="news_api")
app.register_blueprint(game_bp, url_prefix="/api", name="game_api")
app.register_blueprint(event_bp, url_prefix="/api", name="event_api")

if __name__ == "__main__":
    with app.app_context():
        logger.info("Registered Endpoints:")
        for rule in app.url_map.iter_rules():
            logger.info(f"Endpoint: {rule.endpoint}, URL: {rule.rule}")
        logger.info("DB initialased")
    app.run(debug=True, port=5000)
