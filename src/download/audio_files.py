import os

import requests

from src.__util import path_of_audio


def __remove_already_exists(data: dict[str, list[str]]) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for language, texts in data.items():
        for text in texts:
            if not os.path.exists(path_of_audio(language, text)):
                if language not in result:
                    result[language] = []
                result[language].append(text)
    return result


def download_audio_files(data: dict[str, list[str]]):
    data = __remove_already_exists(data)
    generate_sound_url = "https://api.soundoftext.com/sounds/"
    download_sound_url = "https://files.soundoftext.com/"

    for language, texts in data.items():
        for text in texts:
            created_sound = requests.post(generate_sound_url, json={"data": {"text": text, "voice": language}})
            get = requests.get(download_sound_url + created_sound.json()["id"] + ".mp3")
            os.makedirs(path_of_audio(language), exist_ok=True)
            with open(path_of_audio(language, text), "wb") as f:
                f.write(get.content)


def download_audio_file(language: str, word: str):
    download_audio_files({language: [word]})
