import logging
from flask import Flask, current_app
from flask_cors import CORS
from flask_wtf import CSRFProtect
from config import Config, TestConfig

from routes.news_admin import news_bp
from routes.auth import auth_bp
from routes.common import common_bp


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Настройка logging
    logger = logging.getLogger(__name__)
    csrf = CSRFProtect(app)
    CORS(app)

    # Регистрация Blueprint
    app.register_blueprint(auth_bp)
    app.register_blueprint(common_bp)
    app.register_blueprint(news_bp)

    with app.app_context():
        Config.configure_logging()
        if config_class.TESTING:
            config_class.configure_logging()
            for rule in app.url_map.iter_rules():
                logging.log(20, f"Endpoint: {rule.endpoint}, URL: {rule.rule}")

    return app


def get_routes():
    output = []
    for rule in current_app.url_map.iter_rules():
        methods = ",".join(sorted(rule.methods))
        endpoint = current_app.view_functions[rule.endpoint]
        metadata = getattr(endpoint, "_metadata", {})
        output.append(
            {
                "endpoint": rule.endpoint,
                "methods": methods,
                "url": rule.rule,
                "name": metadata.get("name", rule.endpoint),
                "category": metadata.get("category", "Utils"),
                "requires_auth": metadata.get("requires_auth", False),
            }
        )
    return output


def inject_routes():
    return {"routes": get_routes()}


# Creating and running the app
if __name__ == "__main__":
    app = create_app()
    app.context_processor(inject_routes)
    app.run(debug=True, port=5001, host="0.0.0.0")
