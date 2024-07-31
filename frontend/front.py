import logging

from flask import Flask, current_app

from config import Config, configure_logging
from routes.auth import auth_bp
from routes.common import common_bp

app = Flask(__name__)

# Настройка logging
configure_logging()
logger = logging.getLogger(__name__)

# Регистрация Blueprint
app.register_blueprint(auth_bp)
app.register_blueprint(common_bp)


def get_routes():
    output = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(sorted(rule.methods))
        endpoint = current_app.view_functions[rule.endpoint]
        metadata = getattr(endpoint, '_metadata', {})
        output.append({
            'endpoint': rule.endpoint,
            'methods': methods,
            'url': rule.rule,
            'name': metadata.get('name', rule.endpoint),
            'category': metadata.get('category', 'Utils'),
            'requires_auth': metadata.get('requires_auth', False)
        })
    return output


@app.context_processor
def inject_routes():
    return {'routes': get_routes()}


if __name__ == '__main__':
    with app.app_context():
        print("FRONTEND ' Registered Endpoints:")
        for rule in app.url_map.iter_rules():
            print(f"Endpoint: {rule.endpoint}, URL: {rule.rule}")
    app.run(debug=True, port=5001)
