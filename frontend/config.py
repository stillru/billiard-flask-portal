import logging


class Config(object):
    CONFIG_NAME = "Default"
    TESTING = True
    DEBUG = True
    PORT = 5001
    LOG_LEVEL = "INFO"
    LOG_FORMAT = (
        "[FRONTEND - Prod] %(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    SECRET_KEY = "just_play"

    @classmethod
    def configure_logging(self):
        logging.basicConfig(level=self.LOG_LEVEL, format=self.LOG_FORMAT)
        logging.log(
            logging.INFO,
            f"Configuration logger done:\t{self.LOG_LEVEL} is set\t Used config - {self.CONFIG_NAME}",
        )

    @classmethod
    def configure_logging(self):
        logging.basicConfig(level=self.LOG_LEVEL, format=self.LOG_FORMAT)
        logging.log(
            logging.INFO,
            f"Configuration logger done:\t{self.LOG_LEVEL} is set\t Used config - {self.CONFIG_NAME}",
        )

        
class TestConfig(Config):
    CONFIG_NAME = "Testing"
    TESTING = True
    LOG_LEVEL = "DEBUG"
    LOG_FORMAT = (
        "[FRONTEND - test] %(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
