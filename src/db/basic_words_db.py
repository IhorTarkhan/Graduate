from src.db import __util as db_util


class BasicWords:
    CREATE_SCRIPT = """
        CREATE TABLE IF NOT EXISTS words_level
        (
            ord   INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE
        );
        
        CREATE TABLE IF NOT EXISTS words_group
        (
            ord        INTEGER PRIMARY KEY AUTOINCREMENT,
            title      TEXT,
            level_name TEXT,
            FOREIGN KEY (level_name) REFERENCES words_level (title)
        );
        
        CREATE TABLE IF NOT EXISTS word
        (
            value      TEXT,
            group_name TEXT,
            FOREIGN KEY (group_name) REFERENCES words_group (title)
        );
    """

    def __init__(self, groups: str, word: str):
        self.groups: str = groups
        self.word: str = word


def insert_word_lever(level: str):
    db_util.change("INSERT INTO words_level(title) VALUES (?);", [level])


def insert_word_group(group: str, level: str):
    db_util.change("INSERT INTO words_group(title, level_name) VALUES (?, ?);", [group, level])


def insert_word_groups(groups: list[str], level: str):
    sql = "INSERT INTO words_group(title, level_name) VALUES {0};".format(("(?, ?), " * len(groups))[:-2])
    parameters = [groups[i // 2] if i % 2 == 0 else level for i in range(len(groups) * 2)]
    db_util.change(sql, parameters)


def insert_word(word: str, group: str):
    db_util.change("INSERT INTO word(value, group_name) VALUES (?, ?);", [word, group])


def insert_words(words: list[str], group: str):
    sql = "INSERT INTO word(value, group_name) VALUES {0};".format(("(?, ?), " * len(words))[:-2])
    parameters = [words[i // 2] if i % 2 == 0 else group for i in range(len(words) * 2)]
    db_util.change(sql, parameters)


def select_level_count() -> int:
    return db_util.select_one_field("SELECT COUNT(*) FROM words_level")


def select_group_count() -> int:
    return db_util.select_one_field("SELECT COUNT(*) FROM words_group")


def select_word_count() -> int:
    return db_util.select_one_field("SELECT COUNT(*) FROM word")
