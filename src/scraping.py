import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

from src.util import get_download_folder


def scrap(data: dict[str, list[str]]) -> None:
    for language, texts in data.items():
        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {"download.default_directory": get_download_folder(language)})
        driver = webdriver.Chrome(options=options)
        driver.get("https://soundoftext.com/")

        def scroll_to(element: WebElement) -> WebElement:
            driver.execute_script("arguments[0].scrollIntoView();", element)
            return element

        text_area = driver.find_element(By.CLASS_NAME, "field__textarea")
        language_select = driver.find_element(By.CLASS_NAME, "field__select")
        submit_button = driver.find_element(By.CLASS_NAME, "field__submit")

        Select(scroll_to(language_select)).select_by_value(language)
        for text in texts:
            scroll_to(text_area).send_keys(text)
            scroll_to(submit_button).click()

        WebDriverWait(driver, 60).until_not(ec.presence_of_element_located((By.CLASS_NAME, "sk-spinner")))
        download_buttons = driver.find_elements(By.XPATH, "//a[@class='card__action' and text()='Download']")
        for download_button in download_buttons:
            scroll_to(download_button).click()
        time.sleep(5)
        driver.quit()
