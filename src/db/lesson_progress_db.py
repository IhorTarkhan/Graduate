from typing import Optional

from src.db import __util as db_util


class LessonProgress:
    CREATE_SCRIPT = """
        CREATE TABLE IF NOT EXISTS lesson_progress
        (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            attempt_id  INTEGER,
            word        TEXT,
            chat_answer TEXT
        );
    """

    def __init__(self, _id: int, word: str, chat_answer: Optional[str]):
        self.id: int = _id
        self.word: str = word
        self.chat_answer: Optional[str] = chat_answer


def insert_new(attempt_id: int, word: str) -> None:
    db_util.change("INSERT INTO lesson_progress(attempt_id, word) VALUES (?, ?);", [attempt_id, word])


def get_active(tg_id: int) -> LessonProgress:
    select = db_util.select_one("""
            SELECT lp.id, lp.word
            FROM lesson_progress lp
                     LEFT JOIN lesson_attempt la on lp.attempt_id = la.id
            WHERE la.tg_id = ? AND lp.chat_answer IS NULL;
        """, [tg_id])
    return LessonProgress(select[0], select[1], None)


def set_chat_answer(_id: int, new_value: str) -> None:
    db_util.change("UPDATE lesson_progress SET chat_answer = ? WHERE id = ?", [new_value, _id])
