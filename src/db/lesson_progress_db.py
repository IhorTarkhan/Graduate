from src.db.Transaction import Transaction


class LessonProgress:
    CREATE_SCRIPT: list[str] = [
        """
            CREATE TABLE IF NOT EXISTS lesson_attempt
            (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                tg_id         INTEGER,
                group_name    TEXT,
                language_code TEXT,
                start         DATE DEFAULT CURRENT_TIMESTAMP
            );
        """,
        """
            CREATE TABLE IF NOT EXISTS lesson_progress
            (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                attempt_id  INTEGER,
                word        TEXT,
                chat_answer TEXT
            );
        """
    ]


def new_attempt(tg_id: int, group_name: str) -> None:
    Transaction.change("""
            INSERT INTO lesson_attempt(tg_id, group_name, language_code)
            SELECT ch.tg_id, ?, ch.language_code
            FROM chat ch
            WHERE tg_id = ?;
    """, [group_name, tg_id])


def select_random_word(tg_id: int) -> str:
    return Transaction.select_one_field("""
            SELECT w.value
            FROM word w
                     LEFT JOIN lesson_attempt la on w.group_name = la.group_name
            WHERE la.tg_id = ?
            ORDER BY la.start DESC, RANDOM()
            LIMIT 1;
    """, [tg_id])


def save_word(tg_id: int, value: str) -> None:
    Transaction.change("""
            INSERT INTO lesson_progress(attempt_id, word)
            SELECT id, ?
            FROM lesson_attempt
            WHERE tg_id = ?
            ORDER BY start DESC
            LIMIT 1;
    """, [value, tg_id])


def delete_last_word(tg_id: int) -> None:
    Transaction.change("""
            DELETE
            FROM lesson_progress
            WHERE id = (SELECT lp.id
                        FROM lesson_progress lp
                                 LEFT JOIN lesson_attempt la on la.id = lp.attempt_id
                        WHERE la.tg_id = ?
                          AND chat_answer IS NULL)
    """, [tg_id])


def save_chat_answer(tg_id: int, answer: str) -> (bool, str):
    select = Transaction.select_one("""
            UPDATE lesson_progress
            SET chat_answer = ?
            WHERE id = (SELECT lp.id
                        FROM lesson_progress lp
                                 LEFT JOIN lesson_attempt la on la.id = lp.attempt_id
                        WHERE la.tg_id = ?
                          AND chat_answer IS NULL)
            RETURNING UPPER(word) == UPPER(chat_answer), word;
    """, [answer, tg_id])
    return bool(select[0]), select[1]


def get_score(tg_id: int) -> (int, int):
    select = Transaction.select_one("""
            SELECT SUM(UPPER(lp.word) == UPPER(lp.chat_answer)), COUNT(*)
            FROM lesson_attempt la
                     LEFT JOIN lesson_progress lp on lp.attempt_id = la.id
            WHERE la.tg_id = ?
            GROUP BY la.start
            ORDER BY la.start DESC
            LIMIT 1;
    """, [tg_id])
    try:
        return int(select[0]), int(select[1])
    except TypeError:
        return 0, 0


def delete_chat_data(tg_id: int) -> None:
    Transaction.change("""
            DELETE FROM lesson_progress
            WHERE id IN (SELECT lp.id
                         FROM lesson_progress lp
                                  LEFT JOIN lesson_attempt la on lp.attempt_id = la.id
                         WHERE la.tg_id = ?);
    """, [tg_id])
    Transaction.change("DELETE FROM lesson_attempt WHERE tg_id = ?;", [tg_id])
