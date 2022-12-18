from typing import Optional

import requests


def sound_audio(language: str, word: str, title: Optional[str] = None) -> str:
    if title is None:
        title = word[:17] + "%2E%2E%2E" if len(word) > 17 else word

    request_data = {"data": {"text": word, "voice": language}}
    created_sound = requests.post("https://api.soundoftext.com/sounds/", json=request_data).json()
    return f"http://ihor-tarkhan.com/files.soundoftext.com/{title}.mp3?id={created_sound['id']}"
