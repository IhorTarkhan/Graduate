import logging

import requests

from src.db import language_db


def download_languages():
    if language_db.find_count() == 0:
        logging.warning("Languages list is empty, start download")
        get = requests.get("https://api.soundoftext.com/voices").json()
        language_db.insert_if_not_exist(list(
            filter(lambda o: o[0] != "ru-RU",
                   map(lambda o: (o["code"], o["name"]),
                       get))))
    else:
        logging.info(f"Skip download languages, already {language_db .find_count()} in db")
