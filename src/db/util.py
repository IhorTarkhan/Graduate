import sqlite3
from contextlib import closing
from typing import Iterable, Any

database_location = "data/database.sqlite"


def select_one(sql: str, parameters: Iterable = ..., pre_query=None) -> Any:
    with closing(sqlite3.connect(database_location)) as connection:
        with closing(connection.cursor()) as cursor:
            if pre_query is not None:
                pre_query(cursor)
            return cursor.execute(sql, parameters).fetchone()


def select(sql: str, parameters: Iterable = ..., pre_query=None) -> list[Any]:
    with closing(sqlite3.connect(database_location)) as connection:
        with closing(connection.cursor()) as cursor:
            if pre_query is not None:
                pre_query(cursor)
            return cursor.execute(sql, parameters).fetchall()


def not_select(sql: str, parameters: Iterable = ..., pre_query=None):
    with closing(sqlite3.connect(database_location)) as connection:
        with closing(connection.cursor()) as cursor:
            if pre_query is not None:
                pre_query(cursor)
            cursor.execute(sql, parameters)
        connection.commit()
