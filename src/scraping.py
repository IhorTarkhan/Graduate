import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


def scrap(text: str, language: str, download_directory: str = None):
    if download_directory is None:
        site = webdriver.Chrome()
    else:
        options = webdriver.ChromeOptions()
        prefs = {"download.default_directory": download_directory}
        options.add_experimental_option("prefs", prefs)
        site = webdriver.Chrome(options=options)

    site.get("https://soundoftext.com/")

    text_area = site.find_element(By.CLASS_NAME, "field__textarea")
    text_area.send_keys(text)

    select = Select(site.find_element(By.CLASS_NAME, "field__select"))
    select.select_by_value(language)

    button = site.find_element(By.CLASS_NAME, "field__submit")
    button.click()
    time.sleep(5)

    play_actions = site.find_element(By.XPATH, "//a[@class='card__action' and text()='Download']")
    site.execute_script("arguments[0].scrollIntoView();", play_actions)
    play_actions.click()
    time.sleep(3)

    print(1)
