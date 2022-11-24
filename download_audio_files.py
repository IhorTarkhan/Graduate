from src.audio.download_audio_files import scrap, fetch
from util import logging_config

if __name__ == "__main__":
    logging_config()
    fetch({"en-US": ["abc", "apple"], "uk-UA": ["кіт", "собака"]})
    scrap({"en-US": ["abc", "apple"], "uk-UA": ["кіт", "собака"]})
