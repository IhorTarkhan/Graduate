import logging
import os


def logging_config() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)25s - %(levelname)8s - %(message)s")


def get_download_folder(language: str) -> str:
    return os.path.join(os.getcwd(), "db/audio_files", language)


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
