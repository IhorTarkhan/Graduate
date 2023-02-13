import urllib.parse
from typing import Optional

import requests


def sound_audio(language: str, word: str, title: Optional[str] = None) -> str:
    if title is None:
        title = word
    title = title[:17] + "..." if len(title) > 17 else title
    title = urllib.parse.quote(title)

    request = {"data": {"text": word, "voice": language}}
    response = requests.post("https://api.soundoftext.com/sounds/", json=request).json()
    # todo error handler (additional request)
    url = f"http://soundoftext.proxy.graduate.ihor-tarkhan.com/{title}.mp3?id={response['id']}"
    return url
