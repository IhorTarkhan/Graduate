from src.db import __util as db_util


class LanguageSelectorState:
    CREATE_SCRIPT = """
        CREATE TABLE IF NOT EXISTS language_selector_state
        (
            chat_id      INTEGER PRIMARY KEY,
            message_id   INTEGER,
            current_page INTEGER
        );
    """

    def __init__(self, chat_id: int, message_id: int, current_page: int):
        self.chat_id: int = chat_id
        self.message_id: int = message_id
        self.current_page: int = current_page


def save(chat_id: int, message_id: int, current_page: int):
    db_util.change("""
            INSERT INTO language_selector_state(chat_id, message_id, current_page)
            VALUES (?, ?, ?)
            ON CONFLICT(chat_id) DO UPDATE SET message_id = ?, current_page = ?;
        """, [chat_id, message_id, current_page, message_id, current_page])


def select_by_chat(chat_id: int) -> LanguageSelectorState:
    select = db_util.select_one(
        "SELECT chat_id, message_id, current_page FROM language_selector_state WHERE chat_id = ?;",
        [chat_id])
    return LanguageSelectorState(select[0], select[1], select[2])


def increase_page(chat_id: int):
    db_util.change(
        "UPDATE language_selector_state SET current_page = current_page + 1 WHERE chat_id = ?;",
        [chat_id])


def decrease_page(chat_id: int):
    db_util.change(
        "UPDATE language_selector_state SET current_page = current_page - 1 WHERE chat_id = ?;",
        [chat_id])
