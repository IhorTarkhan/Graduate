import logging
import sys

import requests


def translate(to: str, word: str) -> str:
    url = "https://google-translate1.p.rapidapi.com/language/translate/v2"

    payload = f"q={word}&target={to}&source=en"
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "application/gzip",
        "X-RapidAPI-Key": sys.argv[2],
        "X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
    }

    response = requests.post(url, data=payload, headers=headers)

    logging.info(response.text)
    return response.json()["data"]["translations"][0]["translatedText"]
