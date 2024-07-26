import logging

from flask import Flask

from config import Config, configure_logging
from routes.auth import auth_bp

app = Flask(__name__)

# Настройка logging
configure_logging()
logger = logging.getLogger(__name__)

# Регистрация Blueprint
app.register_blueprint(auth_bp)



if __name__ == '__main__':
    with app.app_context():
        print("FRONTEND ' Registered Endpoints:")
        for rule in app.url_map.iter_rules():
            print(f"Endpoint: {rule.endpoint}, URL: {rule.rule}")
    app.run(debug=True, port=5001)
