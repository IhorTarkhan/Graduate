import os


def get_download_folder(language: str) -> str:
    return os.path.join(os.getcwd(), "audio_files", language)


def remove_already_exists(data: dict[str, list[str]]) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for language, texts in data.items():
        folder = get_download_folder(language)
        for text in texts:
            if not os.path.exists(os.path.join(folder, text + ".mp3")):
                if language not in result:
                    result[language] = []
                result[language].append(text)
    return result
