from lazy_streams import stream

from src.bot.message_handlers.lesson_progress import REQUIRED_WORDS, REQUIRED_RATE
from src.db.Transaction import Transaction


class BasicWords:
    CREATE_SCRIPT: list[str] = [
        """
            CREATE TABLE IF NOT EXISTS words_level
            (
                ord   INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT UNIQUE
            );
        """,
        """
                CREATE TABLE IF NOT EXISTS words_group
                (
                    ord        INTEGER PRIMARY KEY AUTOINCREMENT,
                    title      TEXT,
                    level_name TEXT,
                    FOREIGN KEY (level_name) REFERENCES words_level (title)
                );
        """,
        """
            CREATE TABLE IF NOT EXISTS word
            (
                value      TEXT,
                group_name TEXT,
                FOREIGN KEY (group_name) REFERENCES words_group (title)
            );
        """
    ]

    def __init__(self, groups: str, word: str):
        self.groups: str = groups
        self.word: str = word


class WordGroup:
    def __init__(self, order: int, level_name: str, title: str, was_success: bool = False):
        self.ord: int = order
        self.level_name: str = level_name
        self.title: str = title
        self.was_success: bool = was_success


def insert_word_lever(level: str):
    Transaction.change("INSERT INTO words_level(title) VALUES (?);", [level])


def insert_word_groups(groups: list[str], level: str):
    sql = "INSERT INTO words_group(title, level_name) VALUES {0};".format(("(?, ?), " * len(groups))[:-2])
    parameters = [groups[i // 2] if i % 2 == 0 else level for i in range(len(groups) * 2)]
    Transaction.change(sql, parameters)


def insert_words(words: list[str], group: str):
    sql = "INSERT INTO word(value, group_name) VALUES {0};".format(("(?, ?), " * len(words))[:-2])
    parameters = [words[i // 2] if i % 2 == 0 else group for i in range(len(words) * 2)]
    Transaction.change(sql, parameters)


def select_level_count() -> int:
    return Transaction.select_one_field("SELECT COUNT(*) FROM words_level")


def select_group_count() -> int:
    return Transaction.select_one_field("SELECT COUNT(*) FROM words_group")


def select_word_count() -> int:
    return Transaction.select_one_field("SELECT COUNT(*) FROM word")


PAGE_SIZE: int = 5


def select_word_groups(chat_id: int, page: int) -> list[WordGroup]:
    select = Transaction.select(""" 
                SELECT ord, level_name, title, SUM(total >= ? AND CAST(success AS REAL) / total > ?) >= 1
                FROM (SELECT wg.ord,
                             wg.level_name,
                             wg.title,
                             SUM(UPPER(lp.word) == UPPER(lp.chat_answer)) AS success,
                             COUNT(*)                                     AS total
                      FROM words_group wg
                               LEFT JOIN lesson_attempt la ON la.group_name = wg.title
                               LEFT JOIN lesson_progress lp ON la.id = lp.attempt_id
                               LEFT JOIN chat c ON c.tg_id = la.tg_id
                      WHERE (c.language_code = la.language_code
                          OR la.language_code IS NULL)
                        AND (c.tg_id = ? OR c.tg_id IS NULL)
                      GROUP BY wg.ord, wg.level_name, wg.title, la.id)
                GROUP BY ord, level_name, title
                ORDER BY ord
                LIMIT ? OFFSET ?;
            """, [REQUIRED_WORDS, REQUIRED_RATE, chat_id, PAGE_SIZE + 1, PAGE_SIZE * page])
    return stream(select) \
        .map(lambda e: WordGroup(e[0], e[1], e[2], bool(e[3]))) \
        .to_list()


def select_random_word(group_name: str) -> str:
    return Transaction.select_one_field(""" 
                SELECT value
                FROM word
                WHERE group_name = ?
                ORDER BY RANDOM()
                LIMIT 1;
            """, [group_name])
