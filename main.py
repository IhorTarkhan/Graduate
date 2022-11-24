from src.fetch import fetch
from src.scraping import scrap
from src.util import logging_config


def main():
    logging_config()
    request = {"en-US": ["abc", "apple"], "uk-UA": ["кіт", "собака"]}
    scrap(request)
    fetch(request)


if __name__ == "__main__":
    main()
