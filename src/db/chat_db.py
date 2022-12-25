from enum import Enum
from typing import Optional

from src.db.Transaction import Transaction


class ChatStatus(Enum):
    NONE = None
    PROCESSING = "PROCESSING"
    STUDYING_LESSON = "STUDYING_LESSON"


class Chat:
    CREATE_SCRIPT: list[str] = [
        """
            CREATE TABLE IF NOT EXISTS chat
            (
                tg_id         INTEGER PRIMARY KEY,
                status        TEXT,
                language_code TEXT NOT NULL DEFAULT 'en-US'
            );
        """
    ]

    def __init__(self, tg_id: int, status: ChatStatus, language_code: str):
        self.tg_id: int = tg_id
        self.status: ChatStatus = status
        self.language_code: str = language_code


def insert_if_not_exist(tg_id: int) -> None:
    Transaction.change("INSERT OR IGNORE INTO chat(tg_id) VALUES (?);", [tg_id])


def upsert(tg_id: int) -> None:
    Transaction.change(
        """
            INSERT INTO chat(tg_id)
            VALUES (?)
            ON CONFLICT(tg_id) DO UPDATE SET status = NULL, language_code = 'en-US'
            WHERE tg_id = ?;
        """, [tg_id, tg_id])


def update_status(tg_id: int, status: ChatStatus) -> None:
    Transaction.change("UPDATE chat SET status = ? WHERE tg_id = ?", [status.value, tg_id])


def update_language_code(tg_id: int, language_code: Optional[str]) -> None:
    Transaction.change("UPDATE chat SET language_code = ? WHERE tg_id = ?", [language_code, tg_id])


def find_by_id(tg_id: int) -> Chat:
    select = Transaction.select_one("SELECT tg_id, status, language_code FROM chat WHERE tg_id = ?", [tg_id])
    return Chat(select[0], ChatStatus(select[1]), select[2])
