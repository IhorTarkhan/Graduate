from src.fetch import fetch
from src.scraping import scrap

if __name__ == '__main__':
    fetch({"en-US": ["abc", "apple"], "uk-UA": ["кіт", "собака"]})
    scrap({"en-US": ["abc", "apple"], "uk-UA": ["кіт", "собака"]})
