import logging


class Config(object):
    '''
    Base configuration class
    '''
    FLASK_ENV = "development"
    DEBUG = False
    TESTING = False
    PORT = 5000
    LOG_LEVEL = logging.INFO
    LOG_FORMAT = "[BACKEND] %(asctime)s - %(name)s - %(levelname)s - %(message)s"
    SECRET_KEY = "just_play"
    token = "eyJhbGciOiAiRWREU0EiLCAidHlwIjogIkpXVCJ9.eyJleHAiOiAxNzU0Mzc0OTUyfQ.cuRAe9wOE_AuJphvR_dN_M_eesJ3KEt_dEDvVBB_mXdWfwZPp6X6fJXNP1gkixCiDt2mWmap1imaS_y69oIkCw"
    SQLALCHEMY_DATABASE_URI = (
        f"sqlite+libsql://localhost:5002/?authToken={token}&secure=false"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    def configure_logging(self):
        logging.basicConfig(level=Config.LOG_LEVEL, format=Config.LOG_FORMAT)


class TestConfig(Config):
    '''
    Test configuration
    '''
    TESTING = True
    LOG_LEVEL = logging.DEBUG
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProductionConfig(Config):
    '''
    Production configuration
    '''
    FLASK_ENV = "production"


class DevelopmentConfig(Config):
    '''
    Development configuration
    '''
    DEBUG = True
