import csv
import datetime

from pathlib import Path
from sqlite3 import Cursor, Connection

from loguru import logger
from weather.utils.time_convert import to_int
JUKORAMA_HEADER = 'Местное время в Жуковском / Раменском (аэропорт)'
TEMP_HEADER = 'T'
SQL_INSERT = """
     INSERT INTO weather (date, time, temperature)
     SELECT ?, ?, ?
     WHERE NOT EXISTS(SELECT 1 FROM weather WHERE date = ? AND time = ?);
 """


def parse_all_csv(cursor: Cursor, path: Path):
    logger.info(f"заполняем базу из .csv используя директорию {path}")
    for file_name in path.glob("*.csv"):
        parse_one_csv(cursor, file_name)


def parse_one_csv(cursor: Cursor, file_name: Path):
    logger.info("используем файл {file_name}", file_name=file_name)
    with file_name.open('r', encoding='utf-8') as in_file:

        # отбрасываем первые 5 строк из-за которых csv не csv
        for _ in range(6):
            in_file.readline()

        reader = csv.DictReader(in_file, delimiter=';', quotechar='"')
        n_lines = 0
        args = []
        for n_lines, line in enumerate(reader):
            this_date, this_time = (line[JUKORAMA_HEADER].split())
            this_date = datetime.datetime.strptime(this_date, "%d.%m.%Y").date().toordinal()
            this_time = datetime.datetime.strptime(this_time, "%H:%M").time()
            minuts = to_int(this_time)

            args.append(make_args_for_request(this_date, minuts, int(float(line[TEMP_HEADER]))))
        cursor.executemany(SQL_INSERT, args)
    logger.info("updated to DB {file_name}. Total {n_lines} lines.", file_name=file_name, n_lines=n_lines)


def make_args_for_request(date_: int, time_: int, temp: int) -> tuple:
    return date_, time_, temp, date_, time_
