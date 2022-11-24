from sqlite3 import Cursor

import db.util as sql_util
from db.chat import Chat


def __create_table_if_not_exists(cursor: Cursor) -> None:
    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS chat
            (
                tg_id       INTEGER PRIMARY KEY,
                last_action TEXT
            );
        """)


def upsert(tg_id: int) -> None:
    sql_util.not_select(
        """
            INSERT INTO chat(tg_id)
            VALUES (?)
            ON CONFLICT(tg_id) DO UPDATE SET last_action=NULL
            WHERE tg_id = ?;
        """, [tg_id, tg_id], __create_table_if_not_exists)


def create_if_not_exist(tg_id: int) -> None:
    sql_util.not_select("INSERT OR IGNORE INTO chat(tg_id) VALUES (?);", [tg_id], __create_table_if_not_exists)


def update_last_action(tg_id: int, last_action: str) -> None:
    sql_util.not_select("UPDATE chat SET last_action = ? WHERE tg_id = ?", [last_action, tg_id],
                        lambda c: create_if_not_exist(tg_id))


def find_by_id(tg_id: int) -> Chat:
    select = sql_util.select_one("SELECT tg_id, last_action FROM chat WHERE tg_id = ?", [tg_id],
                                 lambda c: create_if_not_exist(tg_id))
    return Chat(select[0], select[1])
