import csv
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select

from src.audio.download_audio import get_path


def scrap_options() -> None:
    driver: WebDriver = webdriver.Chrome()
    driver.get("https://soundoftext.com/")

    language_select: WebElement = driver.find_element(By.CLASS_NAME, "field__select")
    driver.execute_script("arguments[0].scrollIntoView();", language_select)
    options: list[WebElement] = Select(language_select).options

    with open(os.path.join(get_path(), "options.csv"), "w") as file:
        writer = csv.writer(file)
        writer.writerows(map(lambda o: [o.get_attribute("value"), o.accessible_name], options))


if __name__ == "__main__":
    scrap_options()
