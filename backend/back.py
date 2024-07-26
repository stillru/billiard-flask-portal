import logging

from flask import Flask
from flask_cors import CORS

from api.player import player_bp
from config import Config, configure_logging
from models import db

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
CORS(app)  # Разрешить междоменные запросы для API

# Настройка logging
configure_logging()
logger = logging.getLogger(__name__)

# Зарегистрируем Blueprint
app.register_blueprint(player_bp, url_prefix='/api')

if __name__ == '__main__':
    with app.app_context():
        print("Registered Endpoints:")
        for rule in app.url_map.iter_rules():
            print(f"Endpoint: {rule.endpoint}, URL: {rule.rule}")
    app.run(debug=True, port=5000)
