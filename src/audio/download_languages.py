import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select

from src.db import language_db


def scrap_languages() -> None:
    driver: WebDriver = webdriver.Chrome()
    driver.get("https://soundoftext.com")

    language_select: WebElement = driver.find_element(By.CLASS_NAME, "field__select")
    driver.execute_script("arguments[0].scrollIntoView();", language_select)
    options: list[WebElement] = Select(language_select).options
    language_db.insert_if_not_exist(list(map(lambda o: (o.get_attribute("value"), o.accessible_name), options)))


def fetch_languages() -> None:
    get = requests.get("https://api.soundoftext.com/voices").json()
    language_db.insert_if_not_exist(list(map(lambda o: (o["code"], o["name"]), get)))
