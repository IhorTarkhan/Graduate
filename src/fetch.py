import os

import requests

from src.util import get_download_folder, remove_already_exists


def fetch(data: dict[str, list[str]]):
    data = remove_already_exists(data)
    generate_sound_url = "https://api.soundoftext.com/sounds/"
    download_sound_url = "https://files.soundoftext.com/"

    for language, texts in data.items():
        for text in texts:
            created_sound = requests.post(generate_sound_url, json={"data": {"text": text, "voice": language}})
            get = requests.get(download_sound_url + created_sound.json()["id"] + ".mp3")
            folder = get_download_folder(language)
            os.makedirs(folder, exist_ok=True)
            path = os.path.join(folder, text + ".mp3")
            with open(path, "wb") as f:
                f.write(get.content)
