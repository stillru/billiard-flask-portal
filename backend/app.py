import logging

from flask import Flask, current_app
from flask_cors import CORS
from flask_migrate import upgrade

from backend.api import player_bp, news_bp, game_bp, event_bp
from backend.extensions import db, migrate
from backend.config import Config, ProductionConfig, TestConfig, DevelopmentConfig


def create_app(config_class=ProductionConfig):
    """
    Function to create the flask application

    :param config_class:
    :param config:
    :return:
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    config_class.configure_logging()
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    with app.app_context():
        app.register_blueprint(player_bp, url_prefix="/api", name="player_api")
        app.register_blueprint(news_bp, url_prefix="/api", name="news_api")
        app.register_blueprint(game_bp, url_prefix="/api", name="game_api")
        app.register_blueprint(event_bp, url_prefix="/api", name="event_api")
        if config_class.TESTING:
            # Initialize the database for testing
            # db.create_all()
            upgrade(directory="backend/migrations")
            config_class.configure_logging()
            for rule in app.url_map.iter_rules():
                logging.log(20, f"Endpoint: {rule.endpoint}, URL: {rule.rule}")
    return app


if __name__ == "__main__":
    app = create_app(ProductionConfig)
    ProductionConfig.configure_logging()
    with app.app_context():
        upgrade(directory="migrations")
        for rule in app.url_map.iter_rules():
            logging.log(20, f"Endpoint: {rule.endpoint}, URL: {rule.rule}")
    app.run(debug=True, port=5000)
