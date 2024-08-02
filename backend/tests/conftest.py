import logging
import os
import sys
import logging
import pytest
from flask_migrate import upgrade


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app import create_app
from backend.extensions import db, migrate

@pytest.fixture(scope="function")
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture(scope="session")
def app():
    app = create_app("config.TestConfig")
    with app.app_context():
        yield app


@pytest.fixture(scope="session")
def _db(app):
    """Create and drop tables for the test database."""
    db.app = app
    db.create_all()
    migrate.init_app(app, db)
    logger = logging.getLogger(__name__)
    logger.info('Created test database')
    upgrade()
    logger.info('Database upgraded with migrations')
    # Print all table names
    print("Tables in the database:")
    for table_name in db.metadata.tables.keys():
        print(table_name)
    yield db

    db.session.remove()
    logger.info('Session removed')
    db.drop_all()
    logger.info('Database dropped')

