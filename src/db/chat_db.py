from typing import Optional

from src.util import db_util


class Chat:
    """
        CREATE TABLE IF NOT EXISTS chat
        (
            tg_id         INTEGER PRIMARY KEY,
            last_action   TEXT,
            language_code TEXT NOT NULL DEFAULT 'en-US'
        );
    """

    def __init__(self, tg_id: int, last_action: str, language_code: str):
        self.tg_id = tg_id
        self.last_action = last_action
        self.language_code = language_code


def insert_if_not_exist(tg_id: int):
    return lambda c: c.execute("INSERT OR IGNORE INTO chat(tg_id) VALUES (?);", [tg_id])


def upsert(tg_id: int) -> None:
    db_util.change(
        """
            INSERT INTO chat(tg_id)
            VALUES (?)
            ON CONFLICT(tg_id) DO UPDATE SET last_action = NULL, language_code = 'en-US'
            WHERE tg_id = ?;
        """, [tg_id, tg_id])


def update_last_action(tg_id: int, last_action: Optional[str]) -> None:
    db_util.change("UPDATE chat SET last_action = ? WHERE tg_id = ?", [last_action, tg_id],
                   insert_if_not_exist(tg_id))


def update_language_code(tg_id: int, language_code: Optional[str]) -> None:
    db_util.change("UPDATE chat SET language_code = ? WHERE tg_id = ?", [language_code, tg_id],
                   insert_if_not_exist(tg_id))


def find_by_id(tg_id: int) -> Chat:
    select = db_util.select_one("SELECT tg_id, last_action, language_code FROM chat WHERE tg_id = ?", [tg_id],
                                insert_if_not_exist(tg_id))
    return Chat(select[0], select[1], select[2])
