import logging
import os
import sys
import time
from multiprocessing import Process
from threading import Thread, Event

import pytest
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.core.os_manager import PATTERN
from webdriver_manager.core.utils import read_version_from_cmd
from webdriver_manager.firefox import GeckoDriverManager

log = logging.getLogger()


@pytest.fixture(scope="session")
def driver(driver_type="Chrome"):
    if driver_type == "Firefox":
        options = webdriver.FirefoxOptions()
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--test-type")
        options.add_argument("--ignore-local-proxy")
        options.binary_location = "/usr/bin/firefox"
        version = read_version_from_cmd(
            "/usr/bin/firefox --version", PATTERN["firefox"]
        )
        driver_binary = GeckoDriverManager(version=version).install()
        driver = webdriver.Firefox(options=options)
    else:
        # set Chrome options to run in headless mode
        options = Options()
        # options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--no-profile")
        # initialize Chrome driver
        driver = webdriver.Chrome(options=options)
    yield driver
    time.sleep(30)
    driver.quit()


def run_backend():
    from backend.config import TestConfig as Backend_TestConfig
    from backend.app import create_app as backend_app

    backend_app = backend_app(Backend_TestConfig)
    backend_app.run(port=5000, use_reloader=False)


def run_frontend():
    from frontend.front import create_app
    from frontend.config import TestConfig

    front_app = create_app(TestConfig)
    front_app.run(port=5001, use_reloader=False)


@pytest.fixture(scope="session")
def backend():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    sys.path.insert(0, project_root)
    backend_process = Process(target=run_backend)
    backend_process.start()
    time.sleep(5)  # Wait for the server to start
    try:
        response = requests.get("http://localhost:5000/")
        if response.status_code == 404:
            log.info("Backend is up and running")
        else:
            log.error("Failed to start backend")
    except Exception as e:
        log.error(f"Failed to connect to backend: {e}")
    yield
    backend_process.terminate()
    backend_process.join()


@pytest.fixture(scope="session")
def frontend():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    sys.path.insert(0, project_root)
    frontend_process = Process(target=run_frontend)
    frontend_process.start()
    time.sleep(5)  # Wait for the server to start
    try:
        response = requests.get("http://localhost:5001/")
        if response.status_code == 200:
            log.info("Frontend is up and running")
        else:
            log.error("Failed to start frontend")
    except Exception as e:
        log.error(f"Failed to connect to frontend: {e}")
    yield
    frontend_process.terminate()
    frontend_process.join()


@pytest.fixture(scope="function")
def client(frontend):
    """A test client for the app."""
    return frontend.test_client()
