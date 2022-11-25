import logging

import src.util.db_util as db_util
from src.db.chat_db import Chat


def _logging_config() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)25s - %(levelname)8s - %(message)s")


def _create_all_tables():
    db_util.change(Chat.__doc__)


def start_util():
    _logging_config()
    _create_all_tables()
