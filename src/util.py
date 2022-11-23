import os


def get_download_folder(language: str) -> str:
    return os.path.join(os.getcwd(), "audio_files", language)
