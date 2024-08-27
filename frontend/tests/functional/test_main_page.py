import os
import sys

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

from selenium.webdriver.support.wait import WebDriverWait

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.insert(0, project_root)

from frontend.tests import log


def test_main_page_selenium(frontend, backend, driver):
    log.info("Start test...")
    driver.get("http://localhost:5001/")
    title = driver.title
    assert "Billijard League - Main Page" in title


def test_add_news_page_selenium(frontend, backend, driver):
    driver.get("http://localhost:5001/add_news")
    title = driver.title
    assert "Billijard League - Add News" in title


def test_add_news_action_page_selenium(frontend, backend, driver):
    driver.get("http://localhost:5001/add_news")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "news-form"))
    )

    # Заполнение формы
    driver.find_element(By.NAME, "title").send_keys("Test News Title")
    driver.find_element(By.NAME, "body").send_keys("This is the body of the test news.")
    driver.find_element(By.NAME, "source_type").send_keys("Source Type")

    # Пример заполнения тегов
    tags_element = driver.find_element(By.NAME, "tags")
    select = Select(tags_element)
    select.select_by_visible_text("Tournament")  # Нажмите Enter для добавления тега

    # Отправка формы
    driver.find_element(By.CSS_SELECTOR, "#submit").click()

    # Проверка отображения уведомления
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#newsToast"))
    )

    toast = driver.find_element(By.CSS_SELECTOR, "#newsToast .toast-body")
    assert toast.text == "Новость успешно добавлена!"
