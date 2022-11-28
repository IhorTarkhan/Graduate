from src.db import __util as db_util


class Language:
    """
        CREATE TABLE IF NOT EXISTS language
        (
            code TEXT PRIMARY KEY,
            name TEXT
        );
    """

    def __init__(self, code: str, name: str):
        self.code: str = code
        self.name: str = name


def insert_if_not_exist(values: list[tuple[str, str]]):
    sql = "INSERT OR IGNORE INTO language(code, name) VALUES {0};".format(", ".join(map(lambda x: "(?, ?)", values)))
    parameters = []
    for code, name in values:
        parameters.append(code)
        parameters.append(name)
    db_util.change(sql, parameters)


def find_all() -> list[Language]:
    return list(map(
        lambda e: Language(e[0], e[1]),
        db_util.select("SELECT code, name FROM language;")
    ))


def find_count() -> int:
    return db_util.select_one_field("SELECT COUNT(code) FROM language;")


def find_all_by_name_like(name: str) -> list[Language]:
    return list(map(
        lambda e: Language(e[0], e[1]),
        db_util.select("SELECT code, name FROM language WHERE name LIKE ?;", ["%" + name + "%"])
    ))
