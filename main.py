from src.fetch import fetch
from src.scraping import scrap


def main():
    fetch({"en-US": ["abc", "apple"], "uk-UA": ["кіт", "собака"]})
    scrap({"en-US": ["abc", "apple"], "uk-UA": ["кіт", "собака"]})


if __name__ == '__main__':
    main()
