from typing import Optional

import src.util.db_util as sql_util
from src.db.chat import Chat


def insert_if_not_exist(tg_id: int):
    return lambda c: c.execute("INSERT OR IGNORE INTO chat(tg_id) VALUES (?);", [tg_id])


def upsert(tg_id: int) -> None:
    sql_util.change(
        """
            INSERT INTO chat(tg_id)
            VALUES (?)
            ON CONFLICT(tg_id) DO UPDATE SET last_action=NULL
            WHERE tg_id = ?;
        """, [tg_id, tg_id])


def update_last_action(tg_id: int, last_action: Optional[str]) -> None:
    sql_util.change("UPDATE chat SET last_action = ? WHERE tg_id = ?", [last_action, tg_id],
                    insert_if_not_exist(tg_id))


def find_by_id(tg_id: int) -> Chat:
    select = sql_util.select_one("SELECT tg_id, last_action FROM chat WHERE tg_id = ?", [tg_id],
                                 insert_if_not_exist(tg_id))
    return Chat(select[0], select[1])
