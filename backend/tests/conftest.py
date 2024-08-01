import logging
import os
import sys

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app import create_app
from backend.extensions import db


@pytest.fixture(scope="function")
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture(scope='session')
def app():
    app = create_app("config.TestConfig")
    with app.app_context():
        yield app

@pytest.fixture(scope='session')
def _db(app):
    """Create and drop tables for the test database."""
    db.app = app
    db.create_all()

    yield db

    db.session.remove()
    db.drop_all()
