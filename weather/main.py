import argparse
import sqlite3
import sys
from sqlite3 import Connection

from PySide2 import QtWidgets

from weather import config
from weather.utils import drop_weather_table, create_weather_table, parse_all_csv, CliTexts
from weather.weather_window import MyWindow

CSV_DIR = config.app_dir.parent / "csv"


def main():
    with sqlite3.connect(config.file_db) as conn:
        cli(conn, config.cli_texts)


def cli(conn: Connection, cli_texts: CliTexts):
    parser = create_parser(cli_texts)
    namespace = parser.parse_args()
    cursor = conn.cursor()
    if namespace.drop:
        drop_weather_table(cursor)
        conn.commit()
    if namespace.create:
        create_weather_table(cursor)
        conn.commit()
    if namespace.fill:
        parse_all_csv(cursor, CSV_DIR)
        conn.commit()
    cursor.close()

    if not namespace.nogui:
        start_window_app(conn)


def create_parser(cli_texts: CliTexts):
    parser = argparse.ArgumentParser(
        prog=cli_texts.program_name,
        description=cli_texts.program_desc,
        epilog=cli_texts.program_ep
    )
    parser.add_argument('-f', '--fill', action='store_const', const=True, help=cli_texts.desc_fill)
    parser.add_argument('-d', '--drop', action='store_const', const=True, help=cli_texts.desc_drop)
    parser.add_argument('-c', '--create', action='store_const', const=True, help=cli_texts.desc_create)
    parser.add_argument('--nogui', action='store_const', const=True, help=cli_texts.desc_nogui)
    return parser


def start_window_app(conn: Connection):
    app = QtWidgets.QApplication([])
    weather = MyWindow(conn, CSV_DIR)
    weather.show()
    sys.exit(app.exec_())
