import os
import logging


class Config:
    DEBUG = True
    PORT = 5000
    LOG_LEVEL = logging.DEBUG
    LOG_FORMAT = "[BACKEND] %(asctime)s - %(name)s - %(levelname)s - %(message)s"
    SECRET_KEY = "just_play"
    token = 'eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjI3MzkyNzZ9.TK17rHBCyk0Fwd8xPozoGZx0hF5EW-d5NVrRNHNzM7LSjVGoMU1szSUC0PYw9ZM9G8iShHgv4D1KQF-0l0NbDw'
    SQLALCHEMY_DATABASE_URI = f'sqlite+libsql://localhost:5002/?authToken={token}&secure=false'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


def configure_logging():
    logging.basicConfig(level=Config.LOG_LEVEL, format=Config.LOG_FORMAT)
