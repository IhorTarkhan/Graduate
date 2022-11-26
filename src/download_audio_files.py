from audio.download_audio_files import fetch_audio_files, scrap_audio_files

if __name__ == "__main__":
    fetch_audio_files({"en-US": ["abc", "apple"], "uk-UA": ["кіт", "собака"]})
    scrap_audio_files({"en-US": ["abc", "apple"], "uk-UA": ["кіт", "собака"]})
