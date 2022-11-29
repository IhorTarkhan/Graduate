import concurrent.futures
import logging
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from src.__util import FirefoxOptions
from src.db import words_groups_db


def __scrap_one_group(link: str, count_log: str):
    logging.info(f"Start  download {count_log}: {link}")
    driver: WebDriver = webdriver.Firefox(options=FirefoxOptions())
    driver.get(link)
    header: str = driver.find_element(By.CLASS_NAME, "page-header").text
    iframe_src = driver.find_elements(By.TAG_NAME, "iframe")[1].get_attribute("src")
    driver.get(iframe_src.replace("_embed", ""))

    WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.TAG_NAME, "li")))

    all_li_tags = driver.find_elements(By.TAG_NAME, "li")
    all_li_tags = all_li_tags[0: int(len(all_li_tags) / 2)]
    words: list[str] = list(map(lambda x: x.text, all_li_tags))
    words: list[str] = list(map(lambda x: x[13:] if x.startswith("Toggle Audio\n") else x, words))
    words_groups_db.insert_if_not_exist(header, words)
    driver.quit()
    logging.info(f"Finish download {count_log}")


def __scrap_word_groups(link: str):
    logging.info(link)

    driver: WebDriver = webdriver.Firefox(options=FirefoxOptions())
    driver.get(link)

    images: list[WebElement] = driver.find_elements(By.CLASS_NAME, "field--name-field-image")
    images.pop()
    images.pop(0)
    links = list(map(lambda x: x.find_element(By.TAG_NAME, "a").get_attribute("href"), images))
    driver.quit()

    with concurrent.futures.ThreadPoolExecutor(os.cpu_count()) as executor:
        futures = []
        for link in links:
            futures.append(executor.submit(__scrap_one_group, link=link, count_log=f"{len(futures) + 1}/{len(links)}"))
        concurrent.futures.wait(futures)
    # for link in links:
    #     __scrap_one_group(link)


def download_word_groups():
    if words_groups_db.select_total_count() != 0:
        groups_count = words_groups_db.select_count_of_groups()
        words_count = words_groups_db.select_total_count()
        logging.info(f"Skip download word groups, already {groups_count} groups with {words_count} words in db")
        return
    logging.warning("Word groups are empty, start download")

    __scrap_word_groups("https://learnenglish.britishcouncil.org/vocabulary/a1-a2-vocabulary")
    logging.info("---------------")
    __scrap_word_groups("https://learnenglish.britishcouncil.org/vocabulary/b1-b2-vocabulary")
