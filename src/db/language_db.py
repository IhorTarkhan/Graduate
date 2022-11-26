import csv
import os

from src.util import db_util


class Language:
    """
        CREATE TABLE IF NOT EXISTS language
        (
            code TEXT PRIMARY KEY,
            name TEXT
        );
    """

    def __init__(self, code: str, name: str):
        self.code = code
        self.name = name


def insert_if_not_exist(values: list[tuple[str, str]]):
    sql = "INSERT OR IGNORE INTO language(code, name) VALUES {0};".format(", ".join(map(lambda x: "(?, ?)", values)))
    parameters = []
    for code, name in values:
        parameters.append(code)
        parameters.append(name)
    db_util.change(sql, parameters)


def find_all() -> list[Language]:
    result: list[Language] = []
    with open(os.path.join("data", "audio_files", "options.csv")) as file:
        for line in csv.reader(file):
            result.append(Language(line[0], line[1]))
    return result


def find_count() -> int:
    return len(find_all())


def find_all_by_name_like(name: str) -> list[Language]:
    result: list[Language] = []
    with open(os.path.join("data", "audio_files", "options.csv")) as file:
        for line in csv.reader(file):
            if name.lower() in line[1].lower():
                result.append(Language(line[0], line[1]))
    return result
