from audio.download_audio_files import fetch_audio_files, scrap_audio_files
from util.start_util import start_util

if __name__ == "__main__":
    start_util()
    fetch_audio_files({"en-US": ["abc", "apple"], "uk-UA": ["кіт", "собака"]})
    scrap_audio_files({"en-US": ["abc", "apple"], "uk-UA": ["кіт", "собака"]})