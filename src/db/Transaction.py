import sqlite3
from sqlite3 import Cursor, Connection
from typing import Any, Optional


class Transaction:
    database_location = "data/database.sqlite"
    connection: Optional[Connection] = None
    cursor: Optional[Cursor] = None

    @staticmethod
    def open() -> None:
        if Transaction.cursor is not None or Transaction.connection is not None:
            raise ValueError("Transaction is already open")
        Transaction.connection = sqlite3.connect(Transaction.database_location)
        Transaction.cursor = Transaction.connection.cursor()

    @staticmethod
    def commit() -> None:
        if Transaction.cursor is None or Transaction.connection is None:
            return
        Transaction.cursor.close()
        Transaction.connection.commit()
        Transaction.connection.close()

        Transaction.cursor = None
        Transaction.connection = None

    @staticmethod
    def rollback() -> None:
        if Transaction.cursor is None or Transaction.connection is None:
            return
        Transaction.cursor.close()
        Transaction.connection.rollback()
        Transaction.connection.close()

        Transaction.cursor = None
        Transaction.connection = None

    @staticmethod
    def select_one(sql: str, parameters: list = ()) -> Any:
        return Transaction.cursor.execute(sql, list(parameters)).fetchone()

    @staticmethod
    def select_one_field(sql: str, parameters: list = ()) -> Any:
        return Transaction.select_one(sql, parameters)[0]

    @staticmethod
    def select(sql: str, parameters: list = ()) -> list[Any]:
        return Transaction.cursor.execute(sql, list(parameters)).fetchall()

    @staticmethod
    def change(sql: str, parameters: list = ()):
        if len(parameters) == 0:
            for s in sql.split(";"):
                Transaction.cursor.execute(s)
        else:
            Transaction.cursor.execute(sql, list(parameters))
