import logging


class Config(object):
    """
    Base configuration class
    """

    LOGGER_NAME = "default_logger"
    FLASK_ENV = "development"
    DEBUG = False
    TESTING = False
    PORT = 5000
    LOG_LEVEL = logging.DEBUG
    LOG_FORMAT = "[BACKEND] %(asctime)s - %(name)s - %(levelname)s - %(message)s"
    SECRET_KEY = "just_play"
    token = "eyJhbGciOiAiRWREU0EiLCAidHlwIjogIkpXVCJ9.eyJleHAiOiAxNzU0Mzc0OTUyfQ.cuRAe9wOE_AuJphvR_dN_M_eesJ3KEt_dEDvVBB_mXdWfwZPp6X6fJXNP1gkixCiDt2mWmap1imaS_y69oIkCw"
    SQLALCHEMY_DATABASE_URI = f"sqlite:///production.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @classmethod
    def configure_logging(cls):
        logging.getLogger(cls.LOGGER_NAME)
        logging.basicConfig(level=cls.LOG_LEVEL, format=cls.LOG_FORMAT)


class TestConfig(Config):
    """
    Test configuration
    """

    LOGGER_NAME = "test_logger"
    TESTING = True
    LOG_LEVEL = logging.DEBUG
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    LOG_FORMAT = "[BACKEND - Test] %(asctime)s - %(name)s - %(levelname)s - %(message)s"


class ProductionConfig(Config):
    """
    Production configuration
    """

    LOGGER_NAME = "prod_logger"
    FLASK_ENV = "production"
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "[BACKEND - Prod] %(asctime)s - %(name)s - %(levelname)s - %(message)s"
    SQLALCHEMY_DATABASE_URI = "sqlite:///production.db"


class DevelopmentConfig(Config):
    """
    Development configuration
    """

    DEBUG = True
