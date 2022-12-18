import sqlite3
from contextlib import closing
from sqlite3 import Cursor
from typing import Any

database_location = "data/database.sqlite"


def select_one(sql: str, parameters: list = ()) -> Any:
    with closing(sqlite3.connect(database_location)) as connection:
        with closing(connection.cursor()) as c:
            cursor: Cursor = c
            return cursor.execute(sql, list(parameters)).fetchone()


def select_one_field(sql: str, parameters: list = ()) -> Any:
    return select_one(sql, parameters)[0]


def select(sql: str, parameters: list = ()) -> list[Any]:
    with closing(sqlite3.connect(database_location)) as connection:
        with closing(connection.cursor()) as c:
            cursor: Cursor = c
            return cursor.execute(sql, list(parameters)).fetchall()


def change(sql: str, parameters: list = ()):
    with closing(sqlite3.connect(database_location)) as connection:
        with closing(connection.cursor()) as c:
            cursor: Cursor = c
            if len(parameters) == 0:
                for s in sql.split(";"):
                    cursor.execute(s)
            else:
                cursor.execute(sql, list(parameters))
        connection.commit()
