import logging


class Config:
    DEBUG = True
    PORT = 5001
    LOG_LEVEL = logging.DEBUG
    LOG_FORMAT = "[FRONTEND] %(asctime)s - %(name)s - %(levelname)s - %(message)s"


def configure_logging():
    logging.basicConfig(level=Config.LOG_LEVEL, format=Config.LOG_FORMAT)
