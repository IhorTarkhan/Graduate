import sqlite3
from sqlite3 import Cursor, Connection
from typing import Any, Optional


class Transaction:
    database_location = "data/database.sqlite"
    connection: Optional[Connection] = None
    cursor: Optional[Cursor] = None

    @staticmethod
    def is_open() -> bool:
        return Transaction.cursor is not None or Transaction.connection is not None

    @staticmethod
    def open() -> None:
        if Transaction.is_open():
            return
        Transaction.connection = sqlite3.connect(Transaction.database_location)
        Transaction.cursor = Transaction.connection.cursor()

    @staticmethod
    def commit() -> None:
        if not Transaction.is_open():
            return
        Transaction.cursor.close()
        Transaction.connection.commit()
        Transaction.connection.close()

        Transaction.cursor = None
        Transaction.connection = None

    @staticmethod
    def rollback() -> None:
        if not Transaction.is_open():
            return
        Transaction.cursor.close()
        Transaction.connection.rollback()
        Transaction.connection.close()

        Transaction.cursor = None
        Transaction.connection = None

    @staticmethod
    def select_one(sql: str, parameters: list = ()) -> Any:
        was_open = Transaction.is_open()
        if not was_open:
            Transaction.open()
        result = Transaction.cursor.execute(sql, list(parameters)).fetchone()
        if not was_open:
            Transaction.commit()
        return result

    @staticmethod
    def select_one_field(sql: str, parameters: list = ()) -> Any:
        was_open = Transaction.is_open()
        if not was_open:
            Transaction.open()
        result = Transaction.select_one(sql, parameters)[0]
        if not was_open:
            Transaction.commit()
        return result

    @staticmethod
    def select(sql: str, parameters: list = ()) -> list[Any]:
        was_open = Transaction.is_open()
        if not was_open:
            Transaction.open()
        result = Transaction.cursor.execute(sql, list(parameters)).fetchall()
        if not was_open:
            Transaction.commit()
        return result

    @staticmethod
    def change(sql: str, parameters: list = ()):
        was_open = Transaction.is_open()
        if not was_open:
            Transaction.open()
        Transaction.cursor.execute(sql, list(parameters))
        if not was_open:
            Transaction.commit()
