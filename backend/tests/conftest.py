import logging
import os
import sys
import logging
import pytest
from flask_migrate import upgrade


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app import create_app
from backend.extensions import db, migrate

logger = logging.getLogger(__name__)


@pytest.fixture(scope="function")
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture(scope="session")
def app():
    app = create_app("config.TestConfig")
    with app.app_context():
        for rule in app.url_map.iter_rules():
            print(f"Endpoint: {rule.endpoint}, URL: {rule.rule}")
        yield app


@pytest.fixture(scope="session")
def _db(app):
    """Create and drop tables for the test database."""
    db.app = app
    db.create_all()
    migrate.init_app(app, db)
    logger.debug("Created test database")
    upgrade()
    logger.debug("Database upgraded with migrations")
    # Print all table names
    print("Tables in the database:")
    for table_name in db.metadata.tables.keys():
        print(table_name)
    try:
        from backend.models import Player

        players = Player.query.all()
        logger.debug(f"Количество записей в таблице Player: {len(players)}")
    except Exception as e:
        logger.error(f"Ошибка при диагностике состояния базы данных: {e}")

    yield db

    db.session.remove()
    logger.debug("Session removed")
    db.drop_all()
    logger.debug("Database dropped")
