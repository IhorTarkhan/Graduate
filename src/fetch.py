import os

import requests

from src.util import get_downloads_folder


def fetch(data: dict[str, list[str]]):
    generate_sound_url = "https://api.soundoftext.com/sounds/"
    download_sound_url = "https://files.soundoftext.com/"

    for language, texts in data.items():
        for text in texts:
            created_sound = requests.post(generate_sound_url, json={"data": {"text": text, "voice": language}})
            get = requests.get(download_sound_url + created_sound.json()["id"] + ".mp3")
            path = os.path.join(get_downloads_folder(), "fetch-" + text + ".mp3")
            with open(path, "wb") as f:
                f.write(get.content)
