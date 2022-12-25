import logging

from src.db import language_db
from src.db.language_db import Language


def insert_basic_languages():
    if language_db.find_count() == 0:
        logging.warning("Languages list is empty, inserting")
        language_db.insert([
            Language("en-US", "English", "en"),
            Language("cmn-Hant-TW", "Chinese", "zh"),
            Language("es-ES", "Spanish", "es"),
            Language("fr-FR", "French", "fr"),
            Language("pt-BR", "Portuguese", "pt"),
            Language("uk-UA", "Ukrainian", "uk"),
            Language("de-DE", "German", "de"),
            Language("it-IT", "Italian", "it"),
            Language("ja-JP", "Japanese", "ja"),
            Language("pl-PL", "Polish", "pl")
        ])
    else:
        logging.info(f"Skip download languages, already {language_db.find_count()} in db")
