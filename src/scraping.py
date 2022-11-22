import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait


def scrap(text: str, language: str):
    driver = webdriver.Chrome()
    driver.get("https://soundoftext.com/")

    def scroll_to(element: WebElement):
        driver.execute_script("arguments[0].scrollIntoView();", element)

    text_area = driver.find_element(By.CLASS_NAME, "field__textarea")
    language_select = Select(driver.find_element(By.CLASS_NAME, "field__select"))
    submit_button = driver.find_element(By.CLASS_NAME, "field__submit")

    text_area.send_keys(text)
    language_select.select_by_value(language)

    submit_button.click()
    WebDriverWait(driver, 50).until_not(ec.presence_of_element_located((By.CLASS_NAME, 'sk-spinner')))

    download_button = driver.find_element(By.XPATH, "//a[@class='card__action' and text()='Download']")
    scroll_to(download_button)
    download_button.click()
    time.sleep(3)
