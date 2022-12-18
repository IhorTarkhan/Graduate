from typing import Optional

import requests


def sound_audio(language: str, word: str, title: Optional[str] = None) -> str:
    if title is None:
        title = word
    title = title[:17] + "%2E%2E%2E" if len(title) > 17 else title

    request_data = {"data": {"text": word, "voice": language}}
    created_sound = requests.post("https://api.soundoftext.com/sounds/", json=request_data).json()
    return f"http://ihor-tarkhan.com/files.soundoftext.com/{title}.mp3?id={created_sound['id']}"
