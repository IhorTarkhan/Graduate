import logging

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select

from src.__util import selenium_chrome_driver_path
from src.db import language_db


def __scrap() -> None:
    driver: WebDriver = webdriver.Chrome(selenium_chrome_driver_path())
    driver.get("https://soundoftext.com")

    language_select: WebElement = driver.find_element(By.CLASS_NAME, "field__select")
    driver.execute_script("arguments[0].scrollIntoView();", language_select)
    options: list[WebElement] = Select(language_select).options
    language_db.insert_if_not_exist(list(map(lambda o: (o.get_attribute("value"), o.accessible_name), options)))


def __fetch() -> None:
    get = requests.get("https://api.soundoftext.com/voices").json()
    language_db.insert_if_not_exist(list(map(lambda o: (o["code"], o["name"]), get)))


def download_languages():
    if language_db.find_count() == 0:
        logging.warning("Languages list is empty, start download")
        __fetch()
        # __scrap()
    else:
        logging.info(f"Skip download languages, already {language_db.find_count()} in db")
