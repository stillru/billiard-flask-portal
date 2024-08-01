import logging


class Config(object):
    FLASK_ENV = "development"
    DEBUG = False
    TESTING = False
    PORT = 5000
    LOG_LEVEL = logging.INFO
    LOG_FORMAT = "[BACKEND] %(asctime)s - %(name)s - %(levelname)s - %(message)s"
    SECRET_KEY = "just_play"
    token = "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjI3MzkyNzZ9.TK17rHBCyk0Fwd8xPozoGZx0hF5EW-d5NVrRNHNzM7LSjVGoMU1szSUC0PYw9ZM9G8iShHgv4D1KQF-0l0NbDw"
    SQLALCHEMY_DATABASE_URI = (
        f"sqlite+libsql://localhost:5002/?authToken={token}&secure=false"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    def configure_logging(self):
        logging.basicConfig(level=Config.LOG_LEVEL, format=Config.LOG_FORMAT)


class TestConfig(Config):
    TESTING = True
    LOG_LEVEL = logging.DEBUG
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProductionConfig(Config):
    FLASK_ENV = "production"


class DevelopmentConfig(Config):
    DEBUG = True
