from src.db import __util as db_util


class WordsGroups:
    """
        CREATE TABLE IF NOT EXISTS words_groups
        (
            groups TEXT,
            word   TEXT,
            UNIQUE(groups, word)
        );
    """

    def __init__(self, groups: str, word: str):
        self.groups: str = groups
        self.word: str = word


def insert_if_not_exist(groups: str, words: list[str]):
    sql = "INSERT OR IGNORE INTO words_groups(groups, word) VALUES {0};".format(
        ", ".join(map(lambda x: "(?, ?)", words)))
    parameters = [words[i // 2] if i % 2 == 1 else groups for i in range(len(words) * 2)]
    db_util.change(sql, parameters)


def select_total_count():
    return db_util.select_one_field("SELECT COUNT(*) FROM words_groups;")


def select_count_of_groups():
    return db_util.select_one_field("SELECT COUNT(DISTINCT groups) FROM words_groups;")
