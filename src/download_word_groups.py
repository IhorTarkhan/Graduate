from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


def download_word_groups():
    driver: WebDriver = webdriver.Chrome()
    driver.get("https://learnenglish.britishcouncil.org/vocabulary/a1-a2-vocabulary")

    images: list[WebElement] = driver.find_elements(By.CLASS_NAME, "field--name-field-image")
    images.pop()
    images.pop(0)
    links = list(map(lambda x: x.find_element(By.TAG_NAME, "a").get_attribute("href"), images))
    for link in links:
        print(link)

    print("---------------")
    driver.get("https://learnenglish.britishcouncil.org/vocabulary/b1-b2-vocabulary")

    images: list[WebElement] = driver.find_elements(By.CLASS_NAME, "field--name-field-image")
    images.pop()
    images.pop(0)
    links = list(map(lambda x: x.find_element(By.TAG_NAME, "a").get_attribute("href"), images))
    for link in links:
        print(link)
