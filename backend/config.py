import os
import logging


class Config:
    DEBUG = True
    PORT = 5000
    LOG_LEVEL = logging.DEBUG
    LOG_FORMAT = "[BACKEND] %(asctime)s - %(name)s - %(levelname)s - %(message)s"
    SECRET_KEY = "just_play"
    SQLALCHEMY_DATABASE_URI = "sqlite:///billiards_league.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


def configure_logging():
    logging.basicConfig(level=Config.LOG_LEVEL, format=Config.LOG_FORMAT)
