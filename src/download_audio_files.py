import os
import threading
import time

import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

from src.__util import path_of_audio, FirefoxDriver


def __remove_already_exists(data: dict[str, list[str]]) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for language, texts in data.items():
        for text in texts:
            if not os.path.exists(path_of_audio(language, text)):
                if language not in result:
                    result[language] = []
                result[language].append(text)
    return result


def __scrap(data: dict[str, list[str]]) -> None:
    data: dict[str, list[str]] = __remove_already_exists(data)
    for language, texts in data.items():
        driver: WebDriver = FirefoxDriver(download_dir=path_of_audio(language))
        driver.get("https://soundoftext.com/")

        def scroll_to(element: WebElement) -> WebElement:
            driver.execute_script("arguments[0].scrollIntoView();", element)
            return element

        text_area: WebElement = driver.find_element(By.CLASS_NAME, "field__textarea")
        language_select: WebElement = driver.find_element(By.CLASS_NAME, "field__select")
        submit_button: WebElement = driver.find_element(By.CLASS_NAME, "field__submit")

        Select(scroll_to(language_select)).select_by_value(language)
        for text in texts:
            scroll_to(text_area).send_keys(text)
            scroll_to(submit_button).click()

        WebDriverWait(driver, 60).until_not(ec.presence_of_element_located((By.CLASS_NAME, "sk-spinner")))
        download_buttons = driver.find_elements(By.XPATH, "//a[@class='card__action' and text()='Download']")
        for download_button in download_buttons:
            scroll_to(download_button).click()

        class MyThread(threading.Thread):
            def run(self):
                time.sleep(3)
                driver.quit()

        MyThread().start()
    time.sleep(3)


def __fetch(data: dict[str, list[str]]):
    data = __remove_already_exists(data)
    generate_sound_url = "https://api.soundoftext.com/sounds/"
    download_sound_url = "https://files.soundoftext.com/"

    for language, texts in data.items():
        for text in texts:
            created_sound = requests.post(generate_sound_url, json={"data": {"text": text, "voice": language}})
            get = requests.get(download_sound_url + created_sound.json()["id"] + ".mp3")
            os.makedirs(path_of_audio(language), exist_ok=True)
            with open(path_of_audio(language, text), "wb") as f:
                f.write(get.content)


def download_audio_files(data: dict[str, list[str]]):
    __fetch(data)
    # __scrap(data)


def download_audio_file(language: str, word: str):
    download_audio_files({language: [word]})
