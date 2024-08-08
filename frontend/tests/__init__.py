import logging

log = logging.getLogger("test_logger")
LOG_FORMAT = "[BACKEND - Test] %(asctime)s - %(name)s - %(levelname)s - %(message)s"
log.setLevel("DEBUG")
logging.basicConfig(format=LOG_FORMAT)
