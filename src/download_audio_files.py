from audio.download_audio_files import fetch, scrap
from util.log_util import logging_config

if __name__ == "__main__":
    logging_config()
    fetch({"en-US": ["abc", "apple"], "uk-UA": ["кіт", "собака"]})
    scrap({"en-US": ["abc", "apple"], "uk-UA": ["кіт", "собака"]})
