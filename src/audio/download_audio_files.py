import os

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait


def __remove_already_exists(data: dict[str, list[str]]) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for language, texts in data.items():
        for text in texts:
            if not os.path.exists(path_of(language, text)):
                if language not in result:
                    result[language] = []
                result[language].append(text)
    return result


def path_of(language: str = None, text: str = None) -> str:
    if language is None:
        return os.path.join(os.getcwd(), "data", "audio_files")
    if text is None:
        return os.path.join(os.getcwd(), "data", "audio_files", language)
    else:
        return os.path.join(os.getcwd(), "data", "audio_files", language, text + ".mp3")


scrap_drivers: dict[str, WebDriver] = {}


def scrap_audio_files(data: dict[str, list[str]]) -> None:
    data: dict[str, list[str]] = __remove_already_exists(data)
    for language, texts in data.items():
        if language not in scrap_drivers:
            options = webdriver.ChromeOptions()
            options.add_experimental_option("prefs", {"download.default_directory": path_of(language)})
            driver: WebDriver = webdriver.Chrome(options=options)
            driver.get("https://soundoftext.com/")
            scrap_drivers[language] = driver
        driver: WebDriver = scrap_drivers[language]

        def scroll_to(element: WebElement) -> WebElement:
            driver.execute_script("arguments[0].scrollIntoView();", element)
            return element

        text_area: WebElement = driver.find_element(By.CLASS_NAME, "field__textarea")
        language_select: WebElement = driver.find_element(By.CLASS_NAME, "field__select")
        submit_button: WebElement = driver.find_element(By.CLASS_NAME, "field__submit")

        Select(scroll_to(language_select)).select_by_visible_text(language)
        for text in texts:
            scroll_to(text_area).send_keys(text)
            scroll_to(submit_button).click()

        WebDriverWait(driver, 60).until_not(ec.presence_of_element_located((By.CLASS_NAME, "sk-spinner")))
        download_buttons = driver.find_elements(By.XPATH, "//a[@class='card__action' and text()='Download']")
        for download_button in download_buttons:
            scroll_to(download_button).click()


def fetch_audio_files(data: dict[str, list[str]]):
    data = __remove_already_exists(data)
    generate_sound_url = "https://api.soundoftext.com/sounds/"
    download_sound_url = "https://files.soundoftext.com/"

    for language, texts in data.items():
        for text in texts:
            created_sound = requests.post(generate_sound_url, json={"data": {"text": text, "voice": language}})
            get = requests.get(download_sound_url + created_sound.json()["id"] + ".mp3")
            os.makedirs(path_of(language), exist_ok=True)
            with open(path_of(language, text), "wb") as f:
                f.write(get.content)
