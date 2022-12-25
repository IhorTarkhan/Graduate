from lazy_streams import stream

from src.db.Transaction import Transaction


class Language:
    CREATE_SCRIPT: list[str] = [
        """
            CREATE TABLE IF NOT EXISTS language
            (
                code               TEXT PRIMARY KEY,
                name               TEXT,
                translate_api_code TEXT
            );
        """
    ]

    def __init__(self, code: str, name: str, translate_api_code: str):
        self.code: str = code
        self.name: str = name
        self.translate_api_code: str = translate_api_code


def insert(values: list[Language]):
    sql = "INSERT INTO language(code, name, translate_api_code) VALUES {0};" \
        .format(", ".join(map(lambda x: "(?, ?, ?)", values)))
    parameters = stream(values) \
        .map(lambda v: [v.code, v.name, v.translate_api_code]) \
        .flatten() \
        .to_list()
    Transaction.change(sql, parameters)


def find_all() -> list[Language]:
    select = Transaction.select("SELECT code, name, translate_api_code FROM language;")
    return stream(select).map(lambda e: Language(e[0], e[1], e[2])).to_list()


def find_count() -> int:
    return Transaction.select_one_field("SELECT COUNT(code) FROM language;")


def find_by_name(name: str) -> Language:
    select = Transaction.select_one("SELECT code, name, translate_api_code FROM language WHERE name = ?;", [name])
    return Language(select[0], select[1], select[2])
