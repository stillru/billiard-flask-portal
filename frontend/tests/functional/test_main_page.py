import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.insert(0, project_root)

from frontend.tests import log


def test_main_page_selenium(frontend, backend, driver):
    log.info("Start test...")
    page = driver.get("http://localhost:5001/")

    # print the HTML of the target webpage
    print(page.status_code)
    # assert "200" in page.status_code
