import datetime
from sqlite3 import Connection

from PySide2 import QtGui
from PySide2.QtCore import QAbstractTableModel, QModelIndex, Qt

from weather.utils.time_convert import to_time


COUNT_IN_HOUR = 2
SQL_ALL_DAY = """
    SELECT 
        time, temperature
    FROM weather 
    WHERE date LIKE ? ORDER BY time
"""


def get_index_by_time(time_: int) -> int:
    return time_ // (60 // COUNT_IN_HOUR)


def get_time_by_index(index: int) -> int:
    return index * 60 // COUNT_IN_HOUR


TIMES = [to_time(get_time_by_index(i)).strftime("%H:%M") for i in range(24 * COUNT_IN_HOUR)]
START_DAY_ROW = 17  # 08:30
MIDDLE_DAY_ROW = 26  # 13:00


class AllDay(QAbstractTableModel):
    def __init__(self, conn: Connection, parent=None, current_date=datetime.datetime.now().date()):
        super().__init__(parent)
        self.conn = conn
        self._array_data = []
        self.headers = ("Температура, °С",)
        self.current_date = current_date.toordinal()
        self.refresh()

    def change_date(self, date_: datetime.date):
        self.current_date = date_.toordinal()
        self.refresh()

    def refresh(self):
        """
        обновляет содержимое модели в соответствии с переданным днём
        :return: None
        """
        cur = self.conn.cursor()
        cur.execute(SQL_ALL_DAY, (self.current_date,))
        self.beginResetModel()
        # self.headers = [column.name for column in cur.description]
        self._array_data = [
            ["---"] for _ in range(24 * COUNT_IN_HOUR)
        ]
        for row in cur:
            self._array_data[get_index_by_time(row[0])][0] = row[1]
        self.endResetModel()
        cur.close()

    # noinspection PyPep8Naming
    def rowCount(self, parent=None, *args, **kwargs):
        return len(self._array_data)

    # noinspection PyPep8Naming
    def columnCount(self, parent=None, *args, **kwargs):
        return len(self._array_data[0])

    def data(self, index: QModelIndex, role=None):
        if not index.isValid():
            return None
        value = self._array_data[index.row()][index.column()]
        if role == Qt.DisplayRole:
            return value
        if role == Qt.BackgroundRole:
            if index.row() == START_DAY_ROW:
                return QtGui.QColor('#A18C3D')
            if index.row() == MIDDLE_DAY_ROW:
                return QtGui.QColor('#e3b918')

        return None

    # noinspection PyPep8Naming
    def headerData(self, col: int, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headers[col]
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return TIMES[col]
        return None

    @property
    def start_day_index(self):
        return self.createIndex(START_DAY_ROW, 0)
