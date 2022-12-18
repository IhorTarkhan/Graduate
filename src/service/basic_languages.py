import logging

from src.db import language_db


def insert_basic_languages():
    if language_db.find_count() == 0:
        logging.warning("Languages list is empty, inserting")
        language_db.insert([
            ("en-US", "English"),
            ("cmn-Hant-TW", "Chinese"),
            ("es-ES", "Spanish"),
            ("fr-FR", "French"),
            ("pt-BR", "Portuguese"),
            ("uk-UA", "Ukrainian"),
            ("de-DE", "German"),
            ("it-IT", "Italian"),
            ("ja-JP", "Japan"),
            ("pl-PL", "Polish")
        ])
    else:
        logging.info(f"Skip download languages, already {language_db.find_count()} in db")
