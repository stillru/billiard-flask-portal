import logging
import os
import sys

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app  # Импорт функции создания приложения
from backend.extensions import db

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@pytest.fixture(scope='session')
def app():
    logger.debug("Создание приложения")
    app = create_app('config.TestConfig')
    with app.app_context():
        logger.debug("Контекст приложения создан")
        yield app
    logger.debug("Контекст приложения завершён")


@pytest.fixture(scope='session')
def tdb(app, db):
    with app.app_context():
        _db = db
        _db.create_all()
        yield _db
        _db.drop_all()

@pytest.fixture(scope='function')
def client(app):
    return app.test_client()
