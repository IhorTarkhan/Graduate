import sqlite3
from contextlib import closing
from sqlite3 import Cursor
from typing import Iterable, Any

database_location = "data/database.sqlite"


def select_one(sql: str, parameters: Iterable = ..., pre_query=None) -> Any:
    with closing(sqlite3.connect(database_location)) as connection:
        with closing(connection.cursor()) as c:
            cursor: Cursor = c
            if pre_query is not None:
                pre_query(cursor)
            return cursor.execute(sql, parameters).fetchone()


def select(sql: str, parameters: Iterable = ..., pre_query=None) -> list[Any]:
    with closing(sqlite3.connect(database_location)) as connection:
        with closing(connection.cursor()) as c:
            cursor: Cursor = c
            if pre_query is not None:
                pre_query(cursor)
            return cursor.execute(sql, parameters).fetchall()


def change(sql: str, parameters: Iterable = (), pre_query=None):
    with closing(sqlite3.connect(database_location)) as connection:
        with closing(connection.cursor()) as c:
            cursor: Cursor = c
            if pre_query is not None:
                pre_query(cursor)
            cursor.execute(sql, parameters)
        connection.commit()
