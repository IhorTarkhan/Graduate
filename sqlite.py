import logging
import sqlite3
from contextlib import closing

from src.util import logging_config


def main():
    logging_config()
    with closing(sqlite3.connect("db/database.sqlite")) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute("CREATE TABLE IF NOT EXISTS fish (name TEXT, species TEXT, tank_number INTEGER)")

            rows = cursor.execute("SELECT name, species, tank_number FROM fish").fetchall()
            logging.info(rows)

            cursor.execute("INSERT INTO fish VALUES ('Sammy', 'shark', 1)")
            cursor.execute("INSERT INTO fish VALUES ('Jamie', 'cuttlefish', 7)")
            rows = cursor.execute("SELECT name, species, tank_number FROM fish").fetchall()
            logging.info(rows)

            rows = cursor.execute("SELECT name, species, tank_number FROM fish WHERE name = ?", ("Jamie",)).fetchall()
            logging.info(rows)

            cursor.execute("UPDATE fish SET tank_number = ? WHERE name = ?", (2, "Sammy"))
            rows = cursor.execute("SELECT name, species, tank_number FROM fish").fetchall()
            logging.info(rows)

            cursor.execute("DELETE FROM fish WHERE name = ?", ("Sammy",))
            rows = cursor.execute("SELECT name, species, tank_number FROM fish").fetchall()
            logging.info(rows)

            cursor.execute("DELETE FROM fish WHERE name = ?", ("Jamie",))
            rows = cursor.execute("SELECT name, species, tank_number FROM fish").fetchall()
            logging.info(rows)


if __name__ == "__main__":
    main()
