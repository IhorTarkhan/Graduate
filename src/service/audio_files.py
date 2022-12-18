import urllib.parse
from typing import Optional

import requests


def sound_audio(language: str, word: str, title: Optional[str] = None) -> str:
    if title is None:
        title = word
    title = title[:17] + "..." if len(title) > 17 else title

    request_data = {"data": {"text": word, "voice": language}}
    created_sound = requests.post("https://api.soundoftext.com/sounds/", json=request_data).json()
    # todo error handler (additional request)
    return f"http://ihor-tarkhan.com/files.soundoftext.com/{urllib.parse.quote(title)}.mp3?id={created_sound['id']}"
