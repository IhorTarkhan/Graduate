import os


def path_of_audio(language: str, text: str = None) -> str:
    if text is None:
        return os.path.join(os.getcwd(), "data", "audio_files", language)
    else:
        return os.path.join(os.getcwd(), "data", "audio_files", language, text + ".mp3")
