from src.db import __util as db_util


class LessonAttempt:
    CREATE_SCRIPT = """
        CREATE TABLE IF NOT EXISTS lesson_attempt
        (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            tg_id      INTEGER,
            group_name TEXT,
            start      DATE DEFAULT CURRENT_TIMESTAMP
        );
    """

    def __init__(self, _id: int, correct_word_count: int, word_count: int, group_name: str):
        self.id: int = _id
        self.correct_word_count: int = correct_word_count
        self.word_count: int = word_count
        self.group_name: str = group_name


def insert_new(tg_id: int, group_name: str) -> None:
    db_util.change("INSERT INTO lesson_attempt(tg_id, group_name) VALUES (?, ?);", [tg_id, group_name])


def get_active(tg_id: int) -> LessonAttempt:
    select = db_util.select_one("""
            SELECT la.id, SUM(upper(lp.word) == upper(lp.chat_answer)), COUNT(*), la.group_name
            FROM lesson_attempt la
                     LEFT JOIN lesson_progress lp on lp.attempt_id = la.id
            WHERE la.tg_id = ?
            GROUP BY la.start
            ORDER BY la.start DESC
            LIMIT 1;
    """, [tg_id])
    return LessonAttempt(select[0], select[1], select[2], select[3])
