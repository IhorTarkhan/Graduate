import concurrent.futures
import logging
import os
from typing import Optional

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from src.db import basic_words_db


class FirefoxDriver(webdriver.Firefox):
    def __init__(self, download_dir: Optional[str] = None):
        options = Options()
        options.add_argument("--headless")
        if download_dir is not None:
            options.set_preference("browser.download.folderList", 2)
            options.set_preference("browser.download.manager.showWhenStarting", False)
            options.set_preference("browser.download.dir", download_dir)
            options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")
        super().__init__(options=options)


def __scrap_one_group(link: str, group: str, count_log: str):
    logging.info(f"Start  download {count_log}: {link}")
    driver: WebDriver = FirefoxDriver()
    driver.get(link)
    iframe_src = driver.find_elements(By.TAG_NAME, "iframe")[1].get_attribute("src")
    driver.get(iframe_src.replace("_embed", ""))

    WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.TAG_NAME, "li")))

    all_li_tags = driver.find_elements(By.TAG_NAME, "li")
    all_li_tags = all_li_tags[0: len(all_li_tags) // 2]
    words: list[str] = list(map(lambda x: x.text.replace("Toggle Audio\n", ""), all_li_tags))
    driver.quit()
    basic_words_db.insert_words(words, group)
    logging.info(f"Finish download {count_log}")


def __scrap_word_groups(level: str):
    logging.info("Start scraping level " + level)
    basic_words_db.insert_word_lever(level)

    driver: WebDriver = FirefoxDriver()
    driver.get(f"https://learnenglish.britishcouncil.org/vocabulary/{level}-vocabulary")

    content_wrappers: list[WebElement] = driver.find_elements(By.CLASS_NAME, "content-wrapper")
    names_links = list(map(lambda x: (x.text.splitlines()[0], x.find_element(By.TAG_NAME, "a").get_attribute("href")),
                           content_wrappers))
    driver.quit()
    basic_words_db.insert_word_groups(list(map(lambda x: x[0], names_links)), level)

    with concurrent.futures.ThreadPoolExecutor(os.cpu_count()) as executor:
        futures = []
        for name_link in names_links:
            print(name_link[1])
            futures.append(executor.submit(__scrap_one_group,
                                           link=name_link[1],
                                           group=name_link[0],
                                           count_log=f"{len(futures) + 1}/{len(names_links)}"))
        concurrent.futures.wait(futures)


def download_basic_words():
    if basic_words_db.select_level_count() == 0:
        logging.warning("Word groups are empty, start download")
        __scrap_word_groups("a1-a2")
        __scrap_word_groups("b1-b2")
    else:
        lc = basic_words_db.select_level_count()
        gc = basic_words_db.select_group_count()
        wc = basic_words_db.select_word_count()
        logging.info(f"Skip download word groups, already levels={lc}, groups={gc}, words={wc} in db")
