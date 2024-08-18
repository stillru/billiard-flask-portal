import logging

from flask import Flask, current_app
from flask_cors import CORS
from flask_migrate import upgrade

from backend.api import player_bp, news_bp, game_bp, event_bp, season_bp
from backend.extensions import db, migrate
from backend.config import Config, ProductionConfig, TestConfig, DevelopmentConfig
from backend.scheduler import start_scheduler
from backend.utils import log


def create_app(config_class=ProductionConfig):
    """
    Function to create the flask application

    :param config_class:
    :param config:
    :return:
    """
    app = Flask(__name__)
    log.info(f"{app.name} is starting...")
    app.config.from_object(config_class)
    log.info(f"Config '{config_class}' configured")
    config_class.configure_logging()
    log.info(f"Logging is configured...")
    db.init_app(app)
    log.info(f"DB initialsed...")
    migrate.init_app(app, db)
    log.info(f"Migrations initilased")
    CORS(app)
    log.info(f"CORS configured")
    with app.app_context():
        start_scheduler(app)
        log.info(f"Scheduler for {app.name} is should be running.")
        app.register_blueprint(player_bp, url_prefix="/api", name="player_api")
        app.register_blueprint(news_bp, url_prefix="/api", name="news_api")
        app.register_blueprint(game_bp, url_prefix="/api", name="game_api")
        app.register_blueprint(event_bp, url_prefix="/api", name="event_api")
        app.register_blueprint(season_bp, url_prefix="/api/", name="season_api")
        if config_class.TESTING:
            # Initialize the database for testing
            # db.create_all()
            upgrade(directory="backend/migrations")
            config_class.configure_logging()
            for item in app.url_map.iter_rules():
                log.info(f"Endpoint: {item.endpoint}, URL: {item.rule}")
    return app


if __name__ == "__main__":
    app = create_app(ProductionConfig)
    ProductionConfig.configure_logging()
    with app.app_context():
        upgrade(directory="migrations")
        for rule in app.url_map.iter_rules():
            logging.log(20, f"Endpoint: {rule.endpoint}, URL: {rule.rule}")
    app.run(debug=True, port=5000)
