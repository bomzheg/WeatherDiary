import datetime
from sqlite3 import Connection


SQL_LAST_DAY = """
    SELECT 
        date
    FROM weather 
    ORDER BY date DESC
    LIMIT 1
"""


def get_last_day(conn: Connection) -> datetime.date:
    cur = conn.cursor()
    cur.execute(SQL_LAST_DAY)
    last_date = cur.fetchone()[0]
    cur.close()
    return datetime.date.fromordinal(last_date)


if __name__ == "__main__":
    import sqlite3
    with sqlite3.connect(r"c:\Users\Public\Python\WeatherDiary.db") as connect:
        d = get_last_day(connect)
    print(d)
