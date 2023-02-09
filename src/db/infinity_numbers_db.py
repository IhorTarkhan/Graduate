from src.db.Transaction import Transaction


class InfinityNumbers:
    CREATE_SCRIPT: list[str] = [
        """
            CREATE TABLE IF NOT EXISTS infinity_numbers
            (
                tg_id       INTEGER PRIMARY KEY,
                range_from  INTEGER,
                range_to    INTEGER,
                last_number INTEGER
            );
        """
    ]

    def __init__(self, tg_id: int, range_from: int, range_to: int):
        self.tg_id: int = tg_id
        self.range_from: int = range_from
        self.range_to: int = range_to


def upsert(val: InfinityNumbers) -> None:
    Transaction.change(
        """
            INSERT INTO infinity_numbers(tg_id, range_from, range_to)
            VALUES (?, ?, ?)
            ON CONFLICT(tg_id) DO UPDATE SET range_from  = ?,
                                             range_to    = ?,
                                             last_number = null
            WHERE tg_id = ?;
        """, [val.tg_id, val.range_from, val.range_to, val.range_from, val.range_to, val.tg_id])


def update_last_number_to(tg_id: int) -> int:
    return Transaction.change("UPDATE infinity_numbers SET last_number = ? WHERE tg_id = ?;", [tg_id])


def get_last_number_to(tg_id: int) -> int:
    return Transaction.select_one_field("SELECT last_number FROM infinity_numbers WHERE tg_id = ?;", [tg_id])
