import os

import requests

from src.__util import path_of_audio


def download_audio_file(language: str, word: str):
    generate_sound_url = "https://api.soundoftext.com/sounds/"
    download_sound_url = "https://files.soundoftext.com/"
    created_sound = requests.post(generate_sound_url, json={"data": {"text": word, "voice": language}})
    get = requests.get(download_sound_url + created_sound.json()["id"] + ".mp3")
    os.makedirs(path_of_audio(language), exist_ok=True)
    with open(path_of_audio(language, word), "wb") as f:
        f.write(get.content)
