from sqlite3 import Connection, Cursor

from loguru import logger


def drop_weather_table(cursor: Cursor):
    cursor.execute("""DROP TABLE weather""")
    logger.debug("Drop Table")


def create_weather_table(cursor: Cursor):
    cursor.execute(
        """
            CREATE TABLE weather (
                date INT NOT NULL,
                time INT NOT NULL,
                temperature INT,
                PRIMARY KEY (date, time)
            )
        """
    )
    logger.debug("Create Table")
