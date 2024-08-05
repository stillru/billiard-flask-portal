import logging

from flask import Flask
from flask_cors import CORS
from flask_migrate import upgrade

from backend.api import player_bp, news_bp, game_bp, event_bp
from backend.extensions import db, migrate
from backend.config import Config


def configure_logging(self):
    '''
    Function to configure the logging for the application

    :param self:
    :return:
    '''
    logging.basicConfig(level=self.LOG_LEVEL, format=self.LOG_FORMAT)


def create_app(config=None):
    '''
    Function to create the flask application

    :param config:
    :return:
    '''
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    if config:
        app.config.from_object(config)
    logger = logging.getLogger(__name__)
    with app.app_context():
        app.register_blueprint(player_bp, url_prefix="/api", name="player_api")
        app.register_blueprint(news_bp, url_prefix="/api", name="news_api")
        app.register_blueprint(game_bp, url_prefix="/api", name="game_api")
        app.register_blueprint(event_bp, url_prefix="/api", name="event_api")
        if 'TestConfig' in config:
            upgrade()
            logger.debug("Database upgraded from migrations...")
            for table_name in db.metadata.tables.keys():
                print(table_name)
    return app


if __name__ == "__main__":
    app = create_app("config.ProductionConfig")
    with app.app_context():
        for rule in app.url_map.iter_rules():
            print(f"Endpoint: {rule.endpoint}, URL: {rule.rule}")
    app.run(debug=True, port=5000)
