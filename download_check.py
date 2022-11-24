from src.audio.download_audio import scrap, fetch
from src.util import logging_config


def main():
    logging_config()
    fetch({"en-US": ["abc", "apple"], "uk-UA": ["кіт", "собака"]})
    scrap({"en-US": ["abc", "apple"], "uk-UA": ["кіт", "собака"]})


if __name__ == "__main__":
    main()
